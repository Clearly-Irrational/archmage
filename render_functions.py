import tcod

#Draw all entities in the list
def render_all(source_con, dest_con, entities_list, game_map, fov_map, fov_recompute, screen_width, screen_height, colors, game_type):
    if fov_recompute:
        # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                #not sure this logic is correct, what about sight blocking but movement non-blocking tiles, example magical darkness?
                wall = game_map.tiles[x][y].block_sight
                #If it's visible make it light colored and mark explored
                if visible:
                    if wall:
                        tcod.console_set_char_background(source_con, x, y, colors.get('light_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(source_con, x, y, colors.get('light_ground'), tcod.BKGND_SET)
                    #Mark tiles as explored
                    game_map.tiles[x][y].explored = True
                #If it is not visible but is explored make it dark colored
                elif game_map.tiles[x][y].explored or game_type == 'viewer':
                    if wall:
                        tcod.console_set_char_background(source_con, x, y, colors.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(source_con, x, y, colors.get('dark_ground'), tcod.BKGND_SET)

    #Draw all entities in the list
    for entity in entities_list:
        draw_entity(source_con, entity, fov_map)

    #Overlay the source console onto the destination console
    source_con.blit(dest=dest_con, width=screen_width, height=screen_height)

#Clear all entities in the list
def clear_all(source_con, entities_list):
    for entity in entities_list:
        clear_entity(source_con, entity)

#Draw a single entity on the source console
def draw_entity(source_con, entity, fov_map):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        #Set the entity color
        source_con.default_fg = (entity.color)
        #Draw this entity on the source console
        tcod.console_put_char(source_con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

#Erase the entity so it won't smear on the next update
def clear_entity(source_con, entity):
    tcod.console_put_char(source_con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
