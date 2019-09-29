import tcod

#Create a fov map so we can track what tiles and entities are visibile
def initialize_fov(game_map):
    fov_map = tcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            #If it's not blocked or block_sight add it to the fov map
            tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight, not game_map.tiles[x][y].blocked)

    return fov_map

#Recalculate what is in fov
def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
