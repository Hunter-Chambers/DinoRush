#############################################################
### IMPORTS
#############################################################
import pygame

import constants


class Parallax:
    #########################################################
    ### PUBLIC INSTANCE METHODS
    #########################################################
    def __init__(self, img_info, loading_on_server=False):
        self.__img = pygame.image.load(
            constants.BASE_PATH
            + f"/assets/imgs/parallaxes/{img_info["img_id"]}.png")
        if (not loading_on_server):
            self.__img = self.__img.convert_alpha()
        # end if

        self.__img = pygame.transform.scale(
            self.__img, (
                self.__img.get_width() * img_info["scale_factor"],
                self.__img.get_height() * img_info["scale_factor"]))

        self.__depth = img_info["depth"]
        self.__scroll_type = img_info["scroll_type"]
        self.__scroll_speed = img_info["scroll_speed"]

        self._rect = pygame.Rect(0, 0, *self.__img.get_size())

        self.__scroll_x = 0
    # end __init__

    def draw(self, screen, camera):
        cam_rect = camera._camera.copy()
        cam_rect.x = -cam_rect.x
        cam_rect.y = -cam_rect.y

        visible_area = self._rect.clip(cam_rect)
        if (visible_area.width > 0 and visible_area.height > 0):
            visible_surface = self.__get_visible_surface(
                visible_area, self._rect)
            screen.blit(visible_surface, camera.apply(visible_area))
        # end if

        # if the visible portion is too small to fill the screen,
        # then do similar calculations to get another visible portion
        # to simulate endless, seamless parallax scrolling
        if (visible_area.width < camera._camera.width):
            extra_rect = self._rect.copy()
            if (self.__scroll_x > cam_rect.x):
                extra_rect.x -= extra_rect.width
            else:
                extra_rect.x += extra_rect.width
            # end if

            visible_area = extra_rect.clip(cam_rect)
            visible_surface = self.__get_visible_surface(
                visible_area, extra_rect)
            screen.blit(visible_surface, camera.apply(visible_area))
        # end if
    # end draw

    def get_depth(self):
        return self.__depth
    # end get_depth

    def get_scroll_type(self):
        return self.__scroll_type
    # end get_scroll_type

    def scroll(self, camera):
        # independent parallaxes scroll continuously
        # (+= scroll_speed)
        if (self.__scroll_type
            == constants.PARALLAX_SCROLL_TYPE_INDEPENDENT_KEYWORD):

            self.__scroll_x += self.__scroll_speed

        # dependent parallaxes scroll based on camera movement
        # (= scroll_speed * camera_movement)
        else:
            self.__scroll_x = (self.__scroll_speed * camera.x)
        # end if

        # reset the horizontal scroll if the parallax
        # image has scrolled out of camera view
        if (self.__scroll_x + self._rect.width < -camera.x):
            self.__scroll_x = -camera.x
        elif (self.__scroll_x > -camera.x + camera.width):
            self.__scroll_x = -camera.x + camera.width

        self._rect.x = int(self.__scroll_x)
    # end scroll

    #########################################################
    ### PRIVATE INSTANCE METHODS
    #########################################################
    def __get_visible_surface(self, visible_area, reference_rect):
        return self.__img.subsurface(visible_area.x - reference_rect.x,
                                     visible_area.y, *visible_area.size)
    # end __get_visible_surface
# end Parallax class