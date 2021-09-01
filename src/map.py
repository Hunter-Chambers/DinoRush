from src.tileset import *


game_map = {}


def load_map(filename):
    f = open('maps/' + filename, 'r')
    lines = f.read()
    f.close()

    lines = lines.split('\n')

    load_tileset('assets/' + lines[0],lines[1].split(','),int(lines[2]),int(lines[3]),int(lines[4]),int(lines[5]), int(lines[6]))
    tile_size = int(lines[2]) * int(lines[6])
    for i in range(6, -1, -1):
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
                # end if

                x += tile_size
            # end for
        # end if
    # end for

# end load_map

def draw_map(screen, layers):
    for layer in layers:
        for tile in game_map[layer]:
            screen.blit(tile_table[tile[0]], tile[1])
        # end for
    # end for

# end draw_map