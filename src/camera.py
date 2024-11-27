#############################################################
### IMPORTS
#############################################################
import constants

import pygame


class Camera:
    #############################################################
    ### PUBLIC INSTANCE METHODS
    #############################################################
    def __init__(self, target_rect, world):
        self._camera = pygame.Rect(0, 0, *constants.WINDOW_SIZE)
        # self._camera = pygame.Rect(0, 0, 1280, 720)
        self.__world = world

        self.update(target_rect)
    # end __init

    def apply(self, entity_rect):
        return entity_rect.move(self._camera.topleft)
    # end apply

    def update(self, target_rect):
        camera_size = self._camera.size
        world_size = self.__world.get_world_size()

        if (world_size[0] <= camera_size[0]
            and world_size[1] <= camera_size[1]):
            self._camera.center = (world_size[0] // 2, world_size[1] // 2)
        else:
            self._camera.x = max(
                camera_size[0] - world_size[0],
                min(0, (camera_size[0] // 2) - target_rect.centerx))
            self._camera.y = max(
                camera_size[1] - world_size[1],
                min(0, (camera_size[1] // 2) - target_rect.centery))
        # end if

        self.__world.scroll_parallaxes(self._camera)
    # end update
# end Camera class