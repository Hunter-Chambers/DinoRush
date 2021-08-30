import pygame


class Tileset:
    def __init__(self, filename, width, height, rows, cols):
        #image = pygame.transform.scale(pygame.image.load(filename).convert(), (640, 384))
        image = pygame.transform.scale(pygame.image.load(filename).convert(), (480, 288))
        self.tile_table = []

        for tile_x in range(0, cols):
            line = []
            self.tile_table.append(line)

            for tile_y in range(0, rows):
                rect = (tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rect))
            # end for

        # end for
    # end __init__

    def get_tile(self, x, y):
        return self.tile_table[x][y]

    # end get_tile

    def draw(self, screen):
        for x, row in enumerate(self.tile_table):
            for y, tile in enumerate(row):
                screen.blit(tile, (x * 72, y * 72))
            # end for
        # end for
    # end draw

# end Tileset class