import pygame

from src import constants


class Game_Map:

    ####################################################
    ### CONSTRUCTOR
    ####################################################
    def __init__(self, filename):
        f = open('assets/maps/' + filename, 'r')
        lines = f.read()
        f.close()
        lines = lines.splitlines()

        f = lines[0]
        tile_names = lines[1].split(',')
        tile_width = int(lines[2])
        tile_height = int(lines[3])
        tile_rows = int(lines[4])
        tile_cols = int(lines[5])
        scale = int(lines[6])
        tile_size = (tile_width * scale, tile_height * scale)

        self.__tile_table = Game_Map.__load_tileset(f, tile_names, tile_width, tile_height, tile_rows, tile_cols, scale)

        self.__map_size = eval(lines[7])
        self.__spawn_points = [eval(i) for i in lines[8].split(';')]

        self.__parallax_imgs = {}
        parallax_amount = int(lines[9])
        for i in range(parallax_amount):
            info = lines[i + 10].split(';')

            if (not info[1] in self.__parallax_imgs):
                image = pygame.Surface(constants.WINDOW_SIZE)
                image.set_colorkey((0,0,0))
                self.__parallax_imgs[info[1]] = [info[2], eval(info[3]), image]
            # end if

            image = pygame.transform.scale(pygame.image.load('assets/maps/parallax/' + info[0]), (constants.WINDOW_SIZE))
            self.__parallax_imgs[info[1]][2].blit(image, (0,0))
        # end for

        self.__display = pygame.Surface(self.__map_size)
        self.__display.set_colorkey((0,0,0))

        extras_amount = int(lines[parallax_amount + 10])
        for i in range(extras_amount):
            info = lines[i + parallax_amount + 11].split(';')

            image = pygame.transform.scale(pygame.image.load('assets/maps/extras/' + info[0]), eval(info[2]))
            self.__display.blit(image, eval(info[1]))
        # end for

        collision_info = {}
        collision_amount = int(lines[parallax_amount + extras_amount + 11])
        for i in range(collision_amount):
            info = lines[i + parallax_amount + extras_amount + 12].split(';')
            collision_info[tuple(info[0].split(','))] = [eval(info[1]), eval(info[2])]
        # end for

        layers = lines[parallax_amount + extras_amount + collision_amount + 12:]

        self.__tile_rects = []

        current_key = None
        game_map = {}

        for layer in layers:
            if ',' not in layer:
                y = 0
                current_key = layer
                game_map[current_key] = []
            else:
                y += tile_size[1]
                x = 0
                layer = layer.split(',')

                for tile in layer:
                    if (tile != '00'):
                        game_map[current_key].append([tile, [x,y]])

                        for collision_set in list(collision_info.keys()):
                            if (tile in collision_set):
                                width = collision_info[collision_set][0][0]
                                height = collision_info[collision_set][0][1]
                                x_offset = collision_info[collision_set][1][0]
                                y_offset = collision_info[collision_set][1][1]
                                self.__tile_rects.append(pygame.Rect(x + x_offset, y + y_offset, width, height))
                            # end if
                        # end for
                    # end if

                    x += tile_size[0]
                # end for
            # end if
        # end for

        for layer in list(game_map.keys()):
            for tile in game_map[layer]:
                self.__display.blit(self.__tile_table[tile[0]], tile[1])
            # end for
        # end for
    # end __init__


    ####################################################
    ### GETTERS
    ####################################################
    def get_tile_rects(self):
        return self.__tile_rects
    # end get_tile_rects


    ####################################################
    ### INSTANCE METHODS
    ####################################################
    def draw(self, screen):
        for group in self.__parallax_imgs:
            screen.blit(self.__parallax_imgs[group][2], (0,0))
        # end for

        screen.blit(self.__display, (0,0))
    # end draw map


    ####################################################
    ### CLASS METHODS
    ####################################################
    def __load_tileset(filename, tile_names, width, height, rows, cols, scale):
        width *= scale
        height *= scale
        image = pygame.transform.scale(pygame.image.load('assets/maps/tilesets/' + filename), (cols * width, rows * height))

        name = 0
        tile_table = {}

        for tile_y in range(0, rows):
            for tile_x in range(0, cols):
                if (tile_names[name] != 'PASS'):
                    rect = (tile_x * width, tile_y * height, width, height)
                    tile_table[tile_names[name]] = image.subsurface(rect)
                # end if

                name += 1
            # end for
        # end for

        return tile_table
    # end load_tileset
# end Game_Map class