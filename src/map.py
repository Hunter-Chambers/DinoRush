import pygame

from src.tileset import *
from src.constants import *


current_map = pygame.Surface(WINDOW_SIZE)
game_map = {}
tile_rects = []

extras = []
collision_info = {}


def load_map(filename):
    f = open('maps/' + filename, 'r')
    lines = f.read()
    f.close()

    lines = lines.split('\n')

    tile_size = int(lines[2]) * int(lines[6])

    load_tileset('assets/imgs/' + lines[0],lines[1].split(','),int(lines[2]),int(lines[3]),int(lines[4]),int(lines[5]),int(lines[6]))

    extras_amount = int(lines[7])
    for i in range(extras_amount):
        f_name, location, scale = lines[i + 8].split(';')
        f_name = pygame.transform.scale(pygame.image.load('assets/imgs/' + f_name), eval(scale))
        extras.append([f_name, eval(location)])
    # end for

    for i in range(7 + extras_amount, -1, -1):
        lines.pop(i)
    # end for

    collision_amount = int(lines[0])
    for i in range(collision_amount):
        tiles, size, offset = lines[i + 1].split(';')
        size = eval(size)
        offset = eval(offset)
        collision_info[tuple(tiles.split(','))] = [size[0], size[1], offset[0], offset[1]]
    # end for

    for i in range(collision_amount, -1, -1):
        lines.pop(i)
    # end for

    current_key = None

    for line in lines:
        if ',' not in line:
            y = 0
            current_key = line
            game_map[current_key] = []
        else:
            y += tile_size
            x = 0
            line = line.split(',')

            for tile in line:
                if (tile != '00'):
                    game_map[current_key].append([tile, [x,y]])

                    for collision_set in list(collision_info.keys()):
                        if (tile in collision_set):
                            width = collision_info[collision_set][0]
                            height = collision_info[collision_set][1]
                            x_offset = collision_info[collision_set][2]
                            y_offset = collision_info[collision_set][3]
                            tile_rects.append(pygame.Rect(x + x_offset, y + y_offset, width, height))
                        # end if
                    # end for
                # end if

                x += tile_size
            # end for
        # end if
    # end for

    if (extras):
        for extra in extras:
            current_map.blit(extra[0], extra[1])
        # end for
    # end if

    for layer in list(game_map.keys()):
        for tile in game_map[layer]:
            current_map.blit(tile_table[tile[0]], tile[1])
        # end for
    # end for

# end load_map

def draw_map(screen):
    screen.blit(current_map, (0,0))
# end draw_map