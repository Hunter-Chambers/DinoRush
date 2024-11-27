#############################################################
### IMPORTS
#############################################################
import constants

import json
import pygame


class Player:
    #########################################################
    ### PUBLIC INSTANCE METHODS
    #########################################################
    def __init__(self, sprite_sheet_id, scale_factor, x, y, multiplayer_id=-1,
                 last_update_timestamp=0, loading_on_server=False):
        self._loaded_on_server = loading_on_server
        self.__character_id = sprite_sheet_id
        self.__scale_factor = scale_factor

        self.__sprite_sheet = pygame.image.load(
            constants.BASE_PATH
            + f"/assets/imgs/sprite_sheets/players/{sprite_sheet_id}.png")
        if (not loading_on_server):
            self.__sprite_sheet = self.__sprite_sheet.convert_alpha()
        # end if

        self.__sprite_sheet = pygame.transform.scale(
            self.__sprite_sheet, (
                self.__sprite_sheet.get_width() * scale_factor,
                self.__sprite_sheet.get_height() * scale_factor))

        sprite_sheet_data_file = open(
            constants.BASE_PATH
            + f"/assets/players/{sprite_sheet_id}_data.json")
        sprite_sheet_data = json.load(sprite_sheet_data_file)
        sprite_sheet_data_file.close()

        self._animations = {}
        self.__load_animations(sprite_sheet_data, scale_factor)

        self._current_frames_id = next(iter(self._animations))
        self._current_frames = self._animations[
            self._current_frames_id]
        self._current_frame = 0
        self._animation_counter = 0  # frame rate

        self._rect = self._current_frames[self._current_frame].get_rect()
        self._rect.topleft = (x, y)

        self._x_vel = 0
        self._y_vel = 0

        self._width_dif = 0
        self._height_dif = 0

        self._multiplayer_id = multiplayer_id

        self._prev_update_pos = self._rect.topleft
        self._last_update_timestamp = last_update_timestamp
        self._prev_update_timestamp = last_update_timestamp

        self._last_render_timestamp = last_update_timestamp
        self._prev_render_timestamp = last_update_timestamp
    # end __init__

    def animate(self, animation_speed):
        # since some animations vary in length,
        # we need to reset the current frame based
        # on the length of the available frames
        self._current_frame = self._current_frame\
            % len(self._current_frames)

        self._animation_counter += 1
        if (self._animation_counter >= animation_speed):
            self._animation_counter = 0
            self._current_frame = (self._current_frame + 1)\
                % len(self._current_frames)
        # end if

        prev_width, prev_height = self._rect.size
        bottom = self._rect.bottom

        self._rect = self.get_image().get_rect(right=self._rect.right)
        self._rect.bottom = bottom

        self._width_dif = max(0, self._rect.width - prev_width)
        self._height_dif = max(0, self._rect.height - prev_height)
    # end animate

    def get_image(self):
        return self._current_frames[self._current_frame]
    # end get_image

    def get_mask(self):
        img = self.get_image()
        return pygame.mask.from_surface(img)
    # end get_mask

    def get_position(self):
        return self._rect.topleft
    # end get_position

    def get_serializable_data(self, pressed_keys=None):
        return {
            "character_id": self.__character_id,
            "scale_factor": self.__scale_factor,
            "position": self._rect.topleft,
            "multiplayer_id": self._multiplayer_id,
            "current_frames_id": self._current_frames_id,
            "current_frame": self._current_frame,
            "animation_counter": self._animation_counter,
            "velocity": (self._x_vel, self._y_vel),
            "size_dif": (self._width_dif, self._height_dif),
            "pressed_keys": pressed_keys
        }
    # end get_serializable_data

    def set_from_unserialized_data(self, player_data, current_time):
        self._prev_update_pos = self.get_position()
        self._prev_update_timestamp = self._last_update_timestamp

        self._rect.topleft = player_data["position"]
        self._current_frames_id = player_data["current_frames_id"]
        self._current_frame = player_data["current_frame"]
        self._animation_counter = player_data["animation_counter"]
        self._x_vel, self._y_vel = player_data["velocity"]
        self._width_dif, self._height_dif = player_data["size_dif"]

        self._current_frames = self._animations[self._current_frames_id]
        self._last_update_timestamp = current_time
    # end set_from_unserialized_data

    #########################################################
    ### PRIVATE INSTANCE METHODS
    #########################################################
    def __get_frame(self, frame_info, scale_factor):
        x = frame_info["x"] * scale_factor
        y = frame_info["y"] * scale_factor
        width = frame_info["width"] * scale_factor
        height = frame_info["height"] * scale_factor
        return self.__sprite_sheet.subsurface(x, y, width, height)
    # end __get_frame

    def __load_animations(self, sprite_sheet_data, scale_factor):
        for animation in sprite_sheet_data:
            self._animations[animation] = []
            for frame_info in sprite_sheet_data[animation]:
                self._animations[animation].append(
                    self.__get_frame(frame_info, scale_factor))
            # end for
        # end for
    # end __load_animations
# end Player class