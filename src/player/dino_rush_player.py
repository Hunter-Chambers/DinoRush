#############################################################
### IMPORTS
#############################################################
import constants
from player.player import Player

import pygame


class DinoRushPlayer(Player):
    __ANIMATION_SPEED = 7  # lower = faster animation
    __GRAVITY = 1
    __TERMINAL_VEL = 20
    __JUMP_POWER = 15
    __WALK_SPEED = 5

    #########################################################
    ### PUBLIC INSTANCE METHODS
    #########################################################
    def __init__(self, sprite_sheet_id, scale_factor, x, y, multiplayer_id=-1,
                 last_update_timestamp=0, loading_on_server=False):
        super().__init__(sprite_sheet_id, scale_factor, x, y, multiplayer_id,
                         last_update_timestamp, loading_on_server)

        self._current_frames = self._animations[
            constants.SPRITE_IDLING_KEYWORD]
        self.__facing_dir = -1

        self._on_ground = False
        self._hit_ceiling = False
    # end __init__

    def animate(self, animation_speed):
        prev_width, prev_height = self._rect.size
        bottom = self._rect.bottom

        super().animate(animation_speed)

        self._rect = self.get_image().get_rect(right=self._rect.right)
        self._rect.bottom = bottom

        self._width_dif = max(0, self._rect.width - prev_width)
        self._height_dif = max(0, self._rect.height - prev_height)
    # end animate

    def draw(self, screen, camera, current_time=None, do_interpolate=False):
        img = self.get_image()
        if (do_interpolate):
            screen.blit(
                img, camera.apply(self.__get_interpolated_rect(current_time)))
        else:
            screen.blit(img, camera.apply(self._rect))
        # end if
    # end draw

    def get_image(self):
        img = super().get_image()
        if (self.__facing_dir < 0):
            img = pygame.transform.flip(img, True, False)
        # end if
        return img
    # end get_image

    def get_mask(self):
        img = self.get_image()
        return pygame.mask.from_surface(img)
    # end get_mask

    def get_serializable_data(self, pressed_keys=None):
        player_data = super().get_serializable_data(pressed_keys)

        player_data["facing_dir"] = self.__facing_dir
        player_data["on_ground"] = self._on_ground
        player_data["hit_ceiling"] = self._hit_ceiling

        return player_data
    # end get_serializable_data

    def set_from_unserialized_data(self, player_data, current_time):
        super().set_from_unserialized_data(player_data, current_time)

        self.__facing_dir = player_data["facing_dir"]
        self._on_ground = player_data["on_ground"]
        self._hit_ceiling = player_data["hit_ceiling"]
    # end set_from_unserialized_data

    def update(self, pressed_keys, current_time):
        self._prev_update_pos = self._rect.topleft
        self._prev_update_timestamp = self._last_update_timestamp

        self.__handle_input(pressed_keys)
        self.animate(DinoRushPlayer.__ANIMATION_SPEED)
        self._rect.x += self._x_vel
        self._rect.y += self._y_vel
        self._last_update_timestamp = current_time
    # end update

    #########################################################
    ### PRIVATE INSTANCE METHODS
    #########################################################
    def __apply_gravity(self):
        if (self._on_ground or self._hit_ceiling):
            return DinoRushPlayer.__GRAVITY
        else:
            return min(DinoRushPlayer.__TERMINAL_VEL,
                       self._y_vel + DinoRushPlayer.__GRAVITY)
    # end __apply_gravity

    def __get_default_frames(self):
        if (self._on_ground):
            self._current_frames_id = constants.SPRITE_IDLING_KEYWORD
        else:
            self._current_frames_id = constants.SPRITE_JUMPING_KEYWORD
        # end if

        return self._animations[self._current_frames_id]
        # end if
    # end __get_default_frames

    def __get_movement_frames(self, is_crouching):
        if (is_crouching):
            self._current_frames_id = constants.SPRITE_CROUCHING_KEYWORD
        else:
            self._current_frames_id = constants.SPRITE_WALKING_KEYWORD
        # end if

        return self._animations[self._current_frames_id]
    # end __get_movement_frames

    def __handle_input(self, pressed_keys):
        self._x_vel = 0
        self._y_vel = self.__apply_gravity()
        self._hit_ceiling = False
        self._current_frames = self.__get_default_frames()

        if (len(pressed_keys)):
            if (pressed_keys[constants.DOWN] and self._on_ground):
                self._current_frames_id = constants.SPRITE_CROUCHED_KEYWORD
                self._current_frames = self._animations[
                    self._current_frames_id]

            if (pressed_keys[constants.LEFT]):
                self._x_vel = -DinoRushPlayer.__WALK_SPEED
                self.__facing_dir = -1
                self._current_frames = self.__get_movement_frames(
                    pressed_keys[constants.DOWN])

            if (pressed_keys[constants.RIGHT]):
                self._x_vel = DinoRushPlayer.__WALK_SPEED
                self.__facing_dir = 1
                self._current_frames = self.__get_movement_frames(
                    pressed_keys[constants.DOWN])

            if (pressed_keys[constants.JUMP] and self._on_ground):
                self._y_vel = -DinoRushPlayer.__JUMP_POWER
                self._current_frames_id = constants.SPRITE_JUMPING_KEYWORD
                self._current_frames = self._animations[
                    self._current_frames_id]
            # end ifs
        # end if
    # end __handle_input

    def __get_interpolated_rect(self, current_time):
        dt = self._last_render_timestamp - self._prev_render_timestamp
        if (dt <= 0): return self._rect
        t = (current_time - self._prev_render_timestamp) / dt
        t = min(max(t, 0), 1)

        prev_x, prev_y = self._prev_update_pos
        current_x, current_y = self._rect.topleft

        interpolated_x = prev_x + ((current_x - prev_x) * t)
        interpolated_y = prev_y + ((current_y - prev_y) * t)

        self._prev_update_pos = (current_x, current_y)
        self._prev_render_timestamp = self._last_render_timestamp
        self._last_render_timestamp = current_time

        return pygame.Rect(interpolated_x, interpolated_y, *self._rect.size)
    # end __get_interpolated_rect
# end DinoRushPlayer class