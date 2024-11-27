#############################################################
### IMPORTS
#############################################################
import pygame

import json
import math

import constants
from world.world_object import WorldObject
from world.parallax import Parallax


class GameWorld:
    #########################################################
    ### PUBLIC INSTANCE METHODS
    #########################################################
    def __init__(self, world_id, loading_on_server=False):
        world_data_file = open(
            constants.BASE_PATH + "/assets/worlds/" + world_id + ".json")
        self.__world_data = json.load(world_data_file)
        world_data_file.close()

        self.__world_objects = {constants.WORLD_BACKGROUND_KEYWORD: [],
                                constants.WORLD_FOREGROUND_KEYWORD: []}
        for object_layer in self.__world_data["object_layers"]:
            for img_info in self.__world_data["object_layers"][object_layer]:
                self.__world_objects[object_layer]\
                    .append(WorldObject(img_info, loading_on_server))
            # end for
        # end for

        self.__parallaxes = {constants.WORLD_BACKGROUND_KEYWORD: [],
                             constants.WORLD_FOREGROUND_KEYWORD: []}
        for parallax_layer in self.__world_data["parallax_layers"]:
            for img_info\
                in self.__world_data["parallax_layers"][parallax_layer]:
                self.__parallaxes[parallax_layer].append(
                    Parallax(img_info, loading_on_server))
            # end for
        # end for

        self.__tile_table = self.__load_tileset(loading_on_server)
        self.__collidable_tile_rects = self.__load_collidable_tile_rects()
    # end __init__

    def draw_background(self, screen, camera):
        self.__draw_parallax_layer(
            screen, camera, constants.WORLD_BACKGROUND_KEYWORD)
        self.__draw_tile_layer(
            screen, camera, constants.WORLD_BACKGROUND_KEYWORD)
        self.__draw_object_layer(
            screen, camera, constants.WORLD_BACKGROUND_KEYWORD)
    # end draw_background

    def draw_foreground(self, screen, camera):
        self.__draw_parallax_layer(
            screen, camera, constants.WORLD_FOREGROUND_KEYWORD)
        self.__draw_tile_layer(
            screen, camera, constants.WORLD_FOREGROUND_KEYWORD)
        self.__draw_object_layer(
            screen, camera, constants.WORLD_FOREGROUND_KEYWORD)
    # end draw_foreground

    def get_collidable_tile_rects(self):
        return self.__collidable_tile_rects.copy()
    # end get_collidable_tile_rects

    def get_world_size(self):
        width = self.__world_data["num_of_cols"]\
            * self.__world_data["scaled_tile_width"]
        height = self.__world_data["num_of_rows"]\
            * self.__world_data["scaled_tile_height"]
        return (width, height)
    # end get_world_size

    def get_tile_size(self):
        width = self.__world_data["scaled_tile_width"]
        height = self.__world_data["scaled_tile_height"]
        return (width, height)
    # end get_tile_size

    def scroll_parallaxes(self, camera):
        for parallax_layer in self.__parallaxes:
            for parallax in self.__parallaxes[parallax_layer]:
                parallax.scroll(camera)
            # end for
        # end for
    # end scroll_parallaxes

    def update(self):
        pass
    # end update

    #########################################################
    ### PRIVATE INSTANCE METHODS
    #########################################################
    def __draw_object_layer(self, screen, camera, layer_name):
        for world_object in sorted(self.__world_objects[layer_name],
                                 key=lambda x: x.get_depth()):
            world_object.draw(screen, camera)
        # end if
    # end __draw_object_layer

    def __draw_parallax_layer(self, screen, camera, layer_name):
        for parallax in sorted(self.__parallaxes[layer_name],
                               key=lambda x: x.get_depth()):
            parallax.draw(screen, camera)
        # end if
    # end draw_parallax_layer

    def __draw_tile_layer(self, screen, camera, layer_name):
        start_col, start_row, end_col, end_row\
            = self.__get_start_and_end_of_viewable_cols_and_rows(camera)
        tile_width, tile_height = self.get_tile_size()

        for layer in self.__world_data["tile_layers"][layer_name]:
            for row in range(start_row, end_row):
                for col in range(start_col, end_col):
                    tile_id = layer[row][col]
                    if (tile_id != constants.BLANK_ID):
                        tile_img = self.__tile_table[tile_id]
                        tile_rect = tile_img.get_rect()
                        tile_rect.x = col * tile_width
                        tile_rect.y = row * tile_height
                        screen.blit(tile_img, camera.apply(tile_rect))
                    # end if
                # end for
            # end for
        # end for
    # end draw_layer

    def __get_start_and_end_of_viewable_cols_and_rows(self, camera):
        tile_width, tile_height = self.get_tile_size()
        world_width, world_height = self.get_world_size()

        start_col = max(0, math.floor(abs(camera._camera.x) / tile_width))
        start_row = max(0, math.floor(abs(camera._camera.y) / tile_height))
        end_col = min(world_width // tile_width,
                      math.ceil(camera._camera.width / tile_width)\
                        + start_col + 1)
        end_row = min(world_height // tile_height,
                      math.ceil(camera._camera.height / tile_height)\
                        + start_row + 1)

        return (start_col, start_row, end_col, end_row)
    # end __get_start_and_end_of_viewable_cols_and_rows

    def __load_collidable_tile_rects(self):
        tile_width, tile_height = self.get_tile_size()
        collidable_tile_rects = []

        for layer_group in self.__world_data["tile_layers"]:
            for tile_layer in self.__world_data["tile_layers"][layer_group]:
                for row in range(len(tile_layer)):
                    for col in range(len(tile_layer[0])):
                        tile_id = tile_layer[row][col]
                        if (tile_id != constants.BLANK_ID
                            and tile_id
                            in self.__world_data["collidable_ids"]):

                            tile_img = self.__tile_table[tile_id]
                            tile_rect = tile_img.get_rect()
                            tile_rect.x = col * tile_width
                            tile_rect.y = row * tile_height
                            collidable_tile_rects.append(tile_rect)
                        # end if
                    # end for
                # end for
            # end for
        # end for

        return collidable_tile_rects
    # end __load_collidable_tile_rects

    def __load_tileset(self, loading_on_server):
        tileset_img = pygame.image.load(
            constants.BASE_PATH
            + f"/assets/imgs/tilesets/{self.__world_data["tileset_id"]}.png")
        if (not loading_on_server):
            tileset_img = tileset_img.convert_alpha()
        # end if

        tileset_img = pygame.transform.scale(
            tileset_img,
            (tileset_img.get_width() * self.__world_data["scale_factor"],
             tileset_img.get_height() * self.__world_data["scale_factor"]))
        
        tile_width, tile_height = self.get_tile_size()
        cols = tileset_img.get_width() // tile_width
        rows = tileset_img.get_height() // tile_height

        tile_table = {}

        for y_offset in range(rows):
            for x_offset in range(cols):
                tile_pos_x = x_offset * tile_width
                tile_pos_y = y_offset * tile_height
                rect = (tile_pos_x, tile_pos_y, tile_width, tile_height)
                tile_id = x_offset + (y_offset * cols) + 1
                tile_table[tile_id] = tileset_img.subsurface(rect)
            # end for
        # end for

        return tile_table
    # end __load_tileset
# end GameWorld class