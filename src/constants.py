####################################################
### IMPORTS
####################################################
import os
import sys


####################################################
### FILE ACCESSOR
####################################################
BASE_PATH = sys._MEIPASS if getattr(sys, "frozen", False)\
        else os.getcwd()


####################################################
### GAME WINDOW
####################################################
GAME_TITLE = "Dino Rush!"
WINDOW_SIZE = (1280, 720)
# WINDOW_SIZE = (1920, 1080)
FPS = 60


####################################################
### NETWORKING
####################################################
SERVER_CONNECTION_INFO = ("192.168.1.80", 27016)
BUFFER_SIZE = 4096

# server codes
LEFT = "LEFT"
DOWN = "DOWN"
RIGHT = "RIGHT"
JUMP = "JUMP"


####################################################
### TILESETS
####################################################
BLANK_ID = 0


####################################################
### SPRITES
####################################################
SPRITE_CROUCHED_KEYWORD = "crouched"
SPRITE_CROUCHING_KEYWORD = "crouching"
SPRITE_DAMAGING_KEYWORD = "damaging"
SPRITE_IDLING_KEYWORD = "idling"
SPRITE_JUMPING_KEYWORD = "jumping"
SPRITE_WALKING_KEYWORD = "walking"


####################################################
### WORLDS
####################################################
WORLD_BACKGROUND_KEYWORD = "background"
WORLD_FOREGROUND_KEYWORD = "foreground"
PARALLAX_SCROLL_TYPE_INDEPENDENT_KEYWORD = "independent"
PARALLAX_SCROLL_TYPE_DEPENDENT_KEYWORD = "dependent"


####################################################
### COLORS
####################################################
COLOR_BLACK = (0, 0, 0)