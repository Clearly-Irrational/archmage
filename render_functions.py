import tcod

#Draw all entities in the list
def render_all(source_con, dest_con, entities_list, game_map, fov_map, fov_recompute, screen_width, screen_height, kolors, game_type, interface_skin, indoors):
    if indoors == True:
        render_all_indoors(source_con, dest_con, entities_list, game_map, fov_map, fov_recompute, screen_width, screen_height, kolors, game_type, interface_skin)
    if indoors == False:
        render_all_outdoors(source_con, dest_con, entities_list, game_map, fov_map, fov_recompute, screen_width, screen_height, kolors, game_type, interface_skin)

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

def render_all_indoors(source_con, dest_con, entities_list, game_map, fov_map, fov_recompute, screen_width, screen_height, kolors, game_type, interface_skin):
    floor_char = chr(298) #256+32+10 (11th char, third row is the empty square)
    if fov_recompute:
        # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                #not sure this logic is correct, what about sight blocking but movement non-blocking tiles, example magical darkness?
                wall = game_map.tiles[x][y].block_sight
                floodfill_done = game_map.tiles[x][y].floodfilled
                #If it's visible make it light colored and mark explored
                if visible:
                    if wall:
                        tcod.console_set_char_background(source_con, x, y, kolors['light_wall'], tcod.BKGND_SET)
                    else:
                        if interface_skin == 'Tutorial':
                            tcod.console_set_char_background(source_con, x, y, kolors['light_ground'], tcod.BKGND_SET)
                        elif interface_skin == 'Graph':
                            tcod.console_set_char_background(source_con, x, y, kolors['console_white'], tcod.BKGND_SET)
                    #Mark tiles as explored
                    game_map.tiles[x][y].explored = True
                #If it is not visible but is explored make it dark colored
                elif game_map.tiles[x][y].explored or game_type == 'viewer':
                    if wall:
                        tcod.console_set_char_background(source_con, x, y, kolors['dark_wall'], tcod.BKGND_SET)
                    elif floodfill_done:
                        tcod.console_set_char_background(source_con, x, y, kolors['purple_fill'], tcod.BKGND_SET)
                    else:
                        if interface_skin == 'Tutorial':
                            tcod.console_set_char_background(source_con, x, y, kolors['dark_ground'], tcod.BKGND_SET)
                        elif interface_skin == 'Graph':
                            tcod.console_set_char_background(source_con, x, y, kolors['console_white'], tcod.BKGND_SET)
    #Draw all entities in the list
    for entity in entities_list:
        draw_entity(source_con, entity, fov_map)

    #Overlay the source console onto the destination console
    source_con.blit(dest=dest_con, width=screen_width, height=screen_height)

def render_all_outdoors(source_con, dest_con, entities_list, game_map, fov_map, fov_recompute, screen_width, screen_height, kolors, game_type, interface_skin):
    floor_char = chr(298) #256+32+10 (11th char, third row is the empty square)
    if fov_recompute:
        # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                #If it's visible make it light colored and mark explored
                if visible:
                    if interface_skin == 'Tutorial':
                        shade = 'light'
                        draw_terrain(source_con, game_map, kolors, x, y, shade)
                    #Mark tiles as explored
                    game_map.tiles[x][y].explored = True
                #If it is not visible but is explored make it dark colored
                elif game_map.tiles[x][y].explored or game_type == 'viewer':
                    if interface_skin == 'Tutorial':
                        shade = 'dark'
                        draw_terrain(source_con, game_map, kolors, x, y, shade)
                    elif interface_skin == 'Graph':
                        tcod.console_put_char_ex(source_con, x, y, floor_char, kolors['dark_ground'], kolors['console_white'])

    #Draw all entities in the list
    for entity in entities_list:
        draw_entity(source_con, entity, fov_map)

    #Overlay the source console onto the destination console
    source_con.blit(dest=dest_con, width=screen_width, height=screen_height)

def draw_terrain(source_con, game_map, kolors, x, y, shade):
    tree_char = chr(288) #256+32 (1st char, third row is the up arrow)
    if game_map.tiles[x][y].vegetation == 0:
        if game_map.tiles[x][y].terrain == 0:
            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_water'], tcod.BKGND_SET)
        elif game_map.tiles[x][y].terrain == 1:
            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_shallows'], tcod.BKGND_SET)
        elif game_map.tiles[x][y].terrain == 2:
            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_sand'], tcod.BKGND_SET)
        elif game_map.tiles[x][y].terrain == 3:
            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_plains'], tcod.BKGND_SET)
        elif game_map.tiles[x][y].terrain == 4:
            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_hills'], tcod.BKGND_SET)
        elif game_map.tiles[x][y].terrain == 5:
            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_mountain'], tcod.BKGND_SET)
        elif game_map.tiles[x][y].terrain == 6:
            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_snow'], tcod.BKGND_SET)
        else:
            print("Uknown terrian type")
    else:
        if game_map.tiles[x][y].terrain == 0:
            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_water'], tcod.BKGND_SET)
        elif game_map.tiles[x][y].terrain == 1:
            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_shallows'], tcod.BKGND_SET)
        elif game_map.tiles[x][y].terrain == 2:
#            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_sand'], tcod.BKGND_SET)
            tcod.console_put_char_ex(source_con, x, y, tree_char, kolors['tree_green'], kolors[shade+'_sand'])
        elif game_map.tiles[x][y].terrain == 3:
#            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_plains'], tcod.BKGND_SET)
            tcod.console_put_char_ex(source_con, x, y, tree_char, kolors['tree_green'], kolors[shade+'_plains'])
        elif game_map.tiles[x][y].terrain == 4:
#            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_hills'], tcod.BKGND_SET)
            tcod.console_put_char_ex(source_con, x, y, tree_char, kolors['tree_green'], kolors[shade+'_hills'])
        elif game_map.tiles[x][y].terrain == 5:
#            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_mountain'], tcod.BKGND_SET)
            tcod.console_put_char_ex(source_con, x, y, tree_char, kolors['tree_green'], kolors[shade+'_mountain'])
        elif game_map.tiles[x][y].terrain == 6:
            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_snow'], tcod.BKGND_SET)
        else:
            print("Uknown terrian type")
