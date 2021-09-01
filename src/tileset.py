import pygame


tile_table = {}


def load_tileset(filename, tile_names, width, height, rows, cols, scale):
    width *= scale
    height *= scale
    image = pygame.transform.scale(pygame.image.load(filename), (cols * width, rows * height))

    name = 0

    for tile_y in range(0, rows):

        for tile_x in range(0, cols):

            if (tile_names[name] != 'PASS'):
                rect = (tile_x * width, tile_y * height, width, height)
                tile_table[tile_names[name]] = image.subsurface(rect)
            # end if

            name += 1

        # end for

    # end for

# end load_tileset