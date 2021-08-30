import pygame
import sys

from src.tileset import Tileset


class DinoRush:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 640))
        self.clock = pygame.time.Clock()

        self.bg_color = pygame.Color('black')

        #self.tiles = Tileset('assets/tileset.png', 64, 64, 6, 10)
        self.tiles = Tileset('assets/tileset.png', 48, 48, 6, 10)

    # end __init__

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # end handle_events

    def update(self):
        pass

    # end update

    def draw(self):
        self.screen.fill(self.bg_color)
        #self.tiles.draw(self.screen)
        self.screen.blit(self.tiles.get_tile(2, 4), (72, 72))
        pygame.display.flip()

    # end draw

# end DinoRush class