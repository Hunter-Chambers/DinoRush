#!/usr/bin/env python


import pygame

from map_editor import map_editor


if (__name__ == "__main__"):
    pygame.init()
    SCREEN = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Tile Map Editor")
    CLOCK = pygame.time.Clock()

    map_editor.main(SCREEN, CLOCK)
# end if