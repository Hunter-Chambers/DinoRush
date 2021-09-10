import pygame


####################################################
### CONSTANTS
####################################################
WINDOW_SIZE = (1536,960)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
SCREEN_CENTER = (768,480)
CLOCK = pygame.time.Clock()
BG_COLOR = pygame.Color('black')
PLAYER_VELOCITY = 5


####################################################
### GLOBALS
####################################################
recv_thread = None
send_thread = None
loop = True

id = None
location = None
img = None
size = None

players = {}