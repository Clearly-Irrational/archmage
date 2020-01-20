import tcod
from enum import Enum

from game_states import GameStates
from menus import inventory_menu

#Set the entity render order
class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def get_names_under_mouse(mouse, entities_list, fov_map):
    (x, y) = (mouse[0], mouse[1])

    names = [entity.name for entity in entities_list
             if entity.x == x and entity.y == y and tcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel_con, x, y, total_width, name, value, maximum, bar_color, back_color):
    #Figure out how wide the bar should be
    bar_width = int(float(value) / maximum * total_width)
    #Create the background
    tcod.console_set_default_background(panel_con, back_color)
    tcod.console_rect(panel_con, x, y, total_width, 1, False, tcod.BKGND_SCREEN)
    #Create the bar
    tcod.console_set_default_background(panel_con, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel_con, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)
    #Print the value
    tcod.console_set_default_foreground(panel_con, tcod.white)
    tcod.console_print_ex(panel_con, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))

#Draw all entities in the list
def render_all(source_con, dest_con, panel_con, entities_list, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, kolors, game_type, interface_skin, indoors, hp_bar_width, panel_height, panel_y, mouse, game_state):
    if indoors == True:
        render_all_indoors(source_con, dest_con, panel_con, entities_list, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, kolors, game_type, interface_skin, hp_bar_width, panel_height, panel_y, mouse)
    if indoors == False:
        render_all_outdoors(source_con, dest_con, panel_con, entities_list, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, kolors, game_type, interface_skin, hp_bar_width, panel_height, panel_y, mouse)

    #Draw all entities in the list
    entities_in_render_order = sorted(entities_list, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(source_con, entity, fov_map)

    #Overlay the source console onto the destination console
    source_con.blit(dest=dest_con, width=screen_width, height=screen_height)

    #Setup the panel console
    panel_con.default_bg = (tcod.black)
    tcod.console_clear(panel_con)

    #Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        panel_con.print(x=message_log.x, y=y, string=message.text, fg=message.color, bg_blend=tcod.BKGND_NONE, alignment=tcod.LEFT)
        y += 1

    #Draw the HP counter
    render_bar(panel_con, 1, 1, hp_bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, tcod.light_red, tcod.darker_red)

    #Write the name of the entity under the mouse cursor
    panel_con.print(x=1, y=0, string=get_names_under_mouse(mouse, entities_list, fov_map), fg=tcod.light_gray, bg_blend=tcod.BKGND_NONE, alignment=tcod.LEFT)

    #Overlay the panel console onto the destination console
    panel_con.blit(dest=dest_con, width=screen_width, height=panel_height, dest_y=panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
           inventory_title = 'Press item letter to use, or Esc to cancel.\n'
        else:
           inventory_title = 'Press item letter to drop it, or Esc to cancel.\n'

        inventory_menu(dest_con, inventory_title, player.inventory, 50, screen_width, screen_height)

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

def render_all_indoors(source_con, dest_con, panel_con, entities_list, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, kolors, game_type, interface_skin, hp_bar_width, panel_height, panel_y, mouse):
    floor_char = chr(298) #256+32+10 (11th char, third row is the empty square)
    if fov_recompute:
        # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                #not sure this logic is correct, what about sight blocking but movement non-blocking tiles, example magical darkness?
                wall = game_map.tiles[x][y].block_sight
                door = game_map.tiles[x][y].door
                floodfill_done = game_map.tiles[x][y].floodfilled
                #If it's visible make it light colored and mark explored
                if visible:
                    if wall:
                        tcod.console_put_char_ex(source_con, x, y, 35, kolors['console_white'], kolors['light_wall'])
                    else:
                        if door:
                            tcod.console_put_char_ex(source_con, x, y, 43, kolors['console_white'], kolors['dark_wall'])
                        else:
                            tcod.console_set_char_background(source_con, x, y, kolors['light_ground'], tcod.BKGND_SET)
                    #Mark tiles as explored
                    game_map.tiles[x][y].explored = True
                #If it is not visible but is explored make it dark colored
                elif game_map.tiles[x][y].explored or game_type == 'viewer':
                    if wall:
                        tcod.console_set_char_background(source_con, x, y, kolors['dark_wall'], tcod.BKGND_SET)
                    elif floodfill_done:
                        tcod.console_set_char_background(source_con, x, y, kolors['purple_fill'], tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(source_con, x, y, kolors['dark_ground'], tcod.BKGND_SET)

def render_all_outdoors(source_con, dest_con, panel_con, entities_list, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, kolors, game_type, interface_skin, hp_bar_width, panel_height, panel_y, mouse):
    floor_char = chr(298) #256+32+10 (11th char, third row is the empty square)
    if fov_recompute:
        # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                #If it's visible make it light colored and mark explored
                if visible:
#                    if interface_skin == 'Tutorial':
                    shade = 'light'
                    draw_terrain(source_con, game_map, kolors, x, y, shade)
                #Mark tiles as explored
                    game_map.tiles[x][y].explored = True
                #If it is not visible but is explored make it dark colored
                elif game_map.tiles[x][y].explored or game_type == 'viewer':
                    shade = 'dark'
                    draw_terrain(source_con, game_map, kolors, x, y, shade)

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
            tcod.console_put_char_ex(source_con, x, y, tree_char, kolors['tree_green'], kolors[shade+'_sand'])
        elif game_map.tiles[x][y].terrain == 3:
            tcod.console_put_char_ex(source_con, x, y, tree_char, kolors['tree_green'], kolors[shade+'_plains'])
        elif game_map.tiles[x][y].terrain == 4:
            tcod.console_put_char_ex(source_con, x, y, tree_char, kolors['tree_green'], kolors[shade+'_hills'])
        elif game_map.tiles[x][y].terrain == 5:
            tcod.console_put_char_ex(source_con, x, y, tree_char, kolors['tree_green'], kolors[shade+'_mountain'])
        elif game_map.tiles[x][y].terrain == 6:
            tcod.console_set_char_background(source_con, x, y, kolors[shade+'_snow'], tcod.BKGND_SET)
        else:
            print("Uknown terrian type")
