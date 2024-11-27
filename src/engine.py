#############################################################
### IMPORTS
#############################################################
import pygame


#############################################################
### PUBLIC METHODS
#############################################################
def draw_hitboxes(screen, camera, world, player):
    for tile_rect in world.get_collidable_tile_rects():
        pygame.draw.rect(
            screen, (255, 255, 255), camera.apply(tile_rect), 2)
    # end for
    pygame.draw.rect(
        screen, (255, 255, 255), camera.apply(player._rect), 2)

    cam_rect = camera._camera.copy()
    cam_rect.x = -cam_rect.x
    cam_rect.y = -cam_rect.y
    pygame.draw.rect(
        screen, (255, 255, 255), camera.apply(cam_rect), 2)
# end draw_hitboxes

def handle_collisions(player, world):
    collidable_tile_rects = world.get_collidable_tile_rects()
    dx = 0
    dy = 0

    player._on_ground = False
    for tile_rect in collidable_tile_rects:
        dx = __calculate_dx(player, tile_rect, dx)
        dy = __calculate_dy(player, tile_rect, dy)
    # end for

    player._rect.x += dx
    player._rect.y += dy
# end handle_collisions

def get_pressed_keys_codes(key_map, pressed_keys):
    mapped_keys = {}
    for server_code, list_of_pygame_keys in key_map.items():
        for pygame_key in list_of_pygame_keys:
            val = mapped_keys.pop(server_code, False)
            mapped_keys[server_code] = val or pressed_keys[pygame_key]
        # end for
    # end for
    return mapped_keys
# end get_pressed_keys_codes


#############################################################
### PRIVATE METHODS
#############################################################
def __calculate_dx(player, tile_rect, initial_dx):
    dx = initial_dx
    x_offset = player._rect.x + dx
    y_offset = player._rect.y - player._y_vel + player._height_dif
    height_offset = player._rect.height - player._height_dif

    if (tile_rect.colliderect(
        x_offset, y_offset, player._rect.width, height_offset)):

        if (player._rect.left < tile_rect.right
              and player._rect.right > tile_rect.right):
            dx = tile_rect.right - player._rect.left

        elif (player._rect.right > tile_rect.left
              and player._rect.left < tile_rect.left):
            dx = tile_rect.left - player._rect.right
        # end if
    # end if

    return dx
# end __calculate_dx

def __calculate_dy(player, tile_rect, initial_dy):
    dy = initial_dy
    x_offset = player._rect.x - player._x_vel + player._width_dif
    y_offset = player._rect.y + dy
    width_offset = player._rect.width - player._width_dif

    if (tile_rect.colliderect(
        x_offset, y_offset, width_offset, player._rect.height)):

        if (player._rect.top < tile_rect.bottom
            and player._rect.bottom > tile_rect.bottom):
            dy = tile_rect.bottom - player._rect.top
            player._hit_ceiling = True

        elif (player._rect.bottom > tile_rect.top
              and player._rect.top < tile_rect.top):
            dy = tile_rect.top - player._rect.bottom
            player._on_ground = True
        # end if
    # end if

    return dy
# end __calculate_dy