def collision_test(rect, tiles):
    hit_list = []

    for tile in tiles:
        if (rect.colliderect(tile)):
            hit_list.append(tile)
        # end if
    # end for

    return hit_list
# end collision_test