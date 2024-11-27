#############################################################
### IMPORTS
#############################################################
import pygame

import constants


class WorldObject:
    #########################################################
    ### PUBLIC INSTANCE METHODS
    #########################################################
    def __init__(self, img_info, loading_on_server=False):
        self.__img = pygame.image.load(
            constants.BASE_PATH
            + f"/assets/imgs/world_objects/{img_info["img_id"]}.png")
        if (not loading_on_server):
            self.__img = self.__img.convert_alpha()
        # end if

        self.__img = pygame.transform.scale(
            self.__img, (
                self.__img.get_width() * img_info["scale_factor"],
                self.__img.get_height() * img_info["scale_factor"]))

        self.__depth = img_info["depth"]

        self._rect = self.__img.get_rect()
        # these are the (x, y) in the world, NOT the screen
        self._rect.topleft = (img_info["x"], img_info["y"])
    # end __init__

    def draw(self, screen, camera):
        cam_rect = camera._camera.copy()
        cam_rect.x = -cam_rect.x
        cam_rect.y = -cam_rect.y

        visible_area = cam_rect.clip(self._rect)
        if (visible_area.width > 0 and visible_area.height > 0):
            x = visible_area.x - self._rect.x
            y = visible_area.y - self._rect.y
            visible_surface = self.__img.subsurface(x, y, *visible_area.size)
            screen.blit(visible_surface, camera.apply(visible_area))
        # end if
    # end draw

    def get_depth(self):
        return self.__depth
    # end get_depth
# end WorldObject class