#############################################################
### IMPORTS
#############################################################
import constants
from entities.entity import Entity


class DinoRushPlayer(Entity):
    __ANIMATION_SPEED = 7  # lower = faster animation
    __GRAVITY = 1
    __TERMINAL_VEL = 20
    __JUMP_POWER = 15
    __WALK_SPEED = 5

    #########################################################
    ### PUBLIC INSTANCE METHODS
    #########################################################
    def __init__(self, sprite_sheet_id, scale_factor, x, y, entity_id=None,
                 loading_on_server=False):
        super().__init__(sprite_sheet_id, scale_factor, x, y, entity_id,
                         loading_on_server)

        self.set_animation_frames(constants.SPRITE_IDLING_KEYWORD)

        self.__on_ground = False
        self.__hit_ceiling = False
    # end __init__

    def get_serializable_data(self):
        player_data = super().get_serializable_data()

        player_data["on_ground"] = self.__on_ground
        player_data["hit_ceiling"] = self.__hit_ceiling

        return player_data
    # end get_serializable_data

    def set_from_unserialized_data(self, player_data):
        super().set_from_unserialized_data(player_data)

        self.__on_ground = player_data["on_ground"]
        self.__hit_ceiling = player_data["hit_ceiling"]
    # end set_from_unserialized_data

    def set_hit_ceiling(self, hit_ceiling):
        self.__hit_ceiling = hit_ceiling
    # end set_hit_ceiling

    def set_on_ground(self, on_ground):
        self.__on_ground = on_ground
    # end set_on_ground

    def update(self, pressed_keys):
        self.__process_inputs(pressed_keys)
        self.animate(DinoRushPlayer.__ANIMATION_SPEED)
    # end update

    #########################################################
    ### PRIVATE INSTANCE METHODS
    #########################################################
    def __apply_gravity(self):
        if (self.__on_ground or self.__hit_ceiling):
            return DinoRushPlayer.__GRAVITY
        else:
            return min(DinoRushPlayer.__TERMINAL_VEL,
                       self.get_velocity()[1] + DinoRushPlayer.__GRAVITY)
    # end __apply_gravity

    def __get_movement_frames_id(self, is_crouching):
        if (is_crouching):
            return constants.SPRITE_CROUCHING_KEYWORD
        else:
            return constants.SPRITE_WALKING_KEYWORD
        # end if
    # end __get_movement_frames_id

    def __process_inputs(self, pressed_keys):
        self.set_x_vel(0)
        self.set_y_vel(self.__apply_gravity())
        self.__hit_ceiling = False
        self.__set_default_frames()

        if (pressed_keys[constants.DOWN] and self.__on_ground):
            self.set_animation_frames(constants.SPRITE_CROUCHED_KEYWORD)
        if (pressed_keys[constants.LEFT]):
            self.set_x_vel(-DinoRushPlayer.__WALK_SPEED)
            self.set_facing_dir(1)
            self.set_animation_frames(
                self.__get_movement_frames_id(pressed_keys[constants.DOWN]))
        if (pressed_keys[constants.RIGHT]):
            self.set_x_vel(DinoRushPlayer.__WALK_SPEED)
            self.set_facing_dir(0)
            self.set_animation_frames(
                self.__get_movement_frames_id(pressed_keys[constants.DOWN]))
        if (pressed_keys[constants.JUMP] and self.__on_ground):
            self.set_y_vel(-DinoRushPlayer.__JUMP_POWER)
            self.set_animation_frames(constants.SPRITE_JUMPING_KEYWORD)
        # end ifs

        self.update_position_by(self.get_velocity())
    # end __process_inputs

    def __set_default_frames(self):
        if (self.__on_ground):
            self.set_animation_frames(constants.SPRITE_IDLING_KEYWORD)
        else:
            self.set_animation_frames(constants.SPRITE_JUMPING_KEYWORD)
        # end if
    # end __set_default_frames
# end DinoRushPlayer class