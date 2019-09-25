import tcod

#Draw all entities in the list
def render_all(source_con, dest_con, entities_list, game_map, screen_width, screen_height, colors):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            #not sure this logic is correct, what about site blocking but movement non-blocking tiles, example magical darkness?
            wall = game_map.tiles[x][y].block_sight

            if wall:
                tcod.console_set_char_background(source_con, x, y, colors.get('dark_wall'), tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(source_con, x, y, colors.get('dark_ground'), tcod.BKGND_SET)

    #Draw all entities in the list
    for entity in entities_list:
        draw_entity(source_con, entity)

    #Overlay the source console onto the destination console
    source_con.blit(dest=dest_con, width=screen_width, height=screen_height)

#Clear all entities in the list
def clear_all(source_con, entities_list):
    for entity in entities_list:
        clear_entity(source_con, entity)

#Draw a single entity on the source console
def draw_entity(source_con, entity):
#    libtcod.console_set_default_foreground(con, entity.color)
    source_con.default_fg = (entity.color)
    #Draw this entity on the source console
    tcod.console_put_char(source_con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

#Erase the entity so it won't smear on the next update
def clear_entity(source_con, entity):
    tcod.console_put_char(source_con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
