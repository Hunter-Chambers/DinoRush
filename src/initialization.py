import pygame
#import sys

#from src.tileset import Tileset
from src.constants import *


def initialize():
    pygame.init()

    pygame.display.set_caption('Dino Rush!')
    pygame.display.set_icon(pygame.image.load('assets/title_icon.png'))

    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

'''
    self.bg_color = pygame.Color('black')
    self.BGBack = pygame.transform.scale(pygame.image.load('assets/BGBack.png'), WINDOW_SIZE)
    self.BGFront = pygame.transform.scale(pygame.image.load('assets/BGFront.png'), WINDOW_SIZE)
    self.CloudsBack = pygame.transform.scale(pygame.image.load('assets/CloudsBack.png'), WINDOW_SIZE)
    self.CloudsFront = pygame.transform.scale(pygame.image.load('assets/CloudsFront.png'), WINDOW_SIZE)

    self.tiles = Tileset(
        'assets/tileset.png',
        ['01','02','03','04','05','06','07','08','PASS','PASS',
            '11','12','13','14','15','16','17','18','PASS','20',
            '21','22','23','24','PASS','PASS','27','28','29','30',
            '31','32','33','34','35','PASS','37','38','39','40',
            '41','42','43','44','45','PASS','47','48','49','50',
            '51','52','53','54','55','56','57','58','PASS','PASS'],
        TILE_SIZE, TILE_SIZE, 6, 10
    )

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
    self.screen.blit(self.CloudsBack, (0,0))
    self.screen.blit(self.CloudsFront, (0,0))
    self.screen.blit(self.BGBack, (0,0))
    self.screen.blit(self.BGFront, (0,0))
    self.screen.blit(self.tiles.get_tile('05'), (72, 72))
    pygame.display.flip()

# end draw
'''