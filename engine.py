import tcod
import tcod.event

from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse
from initialize import get_constants, get_game_variables
from palette import Palette
from render_functions import clear_all, render_all
from caves import Cave
from dungeons import Dungeon
from world import World
from vision import third_eye
from generator import RosterLists
from game_messages import Message

def main():
    #Set the initial variables
    constants = get_constants()
    color_palette = Palette()
    kolors = color_palette.get_colors()
    mod_key = 'none'
    mouse = 'none'
    
    #Build and initialize the random monster rosters
    cr = RosterLists()
    cr.build_roster_lists()
    cr.build_monster_manual()
    current_roster = cr.get_roster_lists()
    current_mm = cr.get_monster_manual()

    #Set the font file and settings
    tcod.console_set_custom_font(constants['font_file'], tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_map_ascii_codes_to_font(256, 32, 0, 1)  #map all characters in 2nd row
    tcod.console_map_ascii_codes_to_font(256+32, 32, 0, 2)  #map all characters in 3rd row

    #Create the screen, the root console
    root_con = tcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['screen_title'], constants['screen_fullscreen'], constants['screen_renderer'], constants['screen_order'], constants['screen_vsync'])

    #Create another console where we'll draw before overlaying it on the root
    main_con = tcod.console.Console(constants['screen_width'], constants['screen_height'], constants['screen_order'])

    #Create panel console for the hp bar and message log
    panel_con = tcod.console.Console(constants['screen_width'], constants['panel_height'], constants['screen_order'])

    #Initialize player, entities, game_map
    player, entities, game_map, indoors, message_log, game_state = get_game_variables(constants, kolors, current_roster, current_mm)

    interface_skin = 'Tutorial' #Choices: Graph, Tutorial

    if interface_skin == 'Graph':
        color_palette.set_color('dark_wall', 70, 130, 180)
        color_palette.set_color('dark_ground', 70, 130, 180)

    #Initialize FOV and calculate on start
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    game_type = 'normal' #choices normal, viewer

    #Initialize the message log
#    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    #Initialize main loop
#    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state
    targeting_item = None
    end_game = False
    while not end_game:
        #Recomput FOV if necessary
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithm'])

        #Render all entities & tiles on main console and blit them to the root console
        render_all(main_con, root_con, panel_con, entities, player, game_map, fov_map, fov_recompute, message_log, constants['screen_width'], constants['screen_height'], kolors, game_type, interface_skin, indoors, constants['hp_bar_width'], constants['panel_height'], constants['panel_y'], mouse, game_state)

        #Reset FOV check
        fov_recompute = False
        #Update the console with our changes
        tcod.console_flush()
        #Erase all entities on main console so they won't smear on next update
        clear_all(main_con, entities)

        #initialize loop variables
        action = {'none': True}
        mouse_action = {'none': True}

        #Detect and handle events
        for event in tcod.event.get():
            if event.type == "QUIT": #Window was closed
                action = {'exit': True}
            elif event.type == "KEYUP" and event.sym == 1073742049:
                mod_key = 'none'
            elif event.type == "KEYDOWN": #A key was depressed
                if event.mod == True and event.sym == 1073742049:
                    mod_key = 'l_shift'
                action = handle_keys(event, mod_key, game_state)
            elif event.type == "MOUSEMOTION": #Mouse was moved
                mouse = event.tile
            elif event.type == "MOUSEBUTTONDOWN":
                mouse = event.tile
                mouse_action = handle_mouse(mouse, event.button)
            #else:
                #print(event)


        #Get action type
        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        exit = action.get('exit')
        error = action.get('error')
        wait = action.get('wait')
        vision = action.get('vision')
        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        #List to store the results of damage
        player_turn_results = []

        #Process player actions
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            #If no terrain is blocking then try to move the player
            if not game_map.is_blocked(destination_x, destination_y):
                #If no entity is blocking then move the player
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    #Recalculate FOV if player moves
                    fov_recompute = True
                game_state = GameStates.ENEMY_TURN
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
 
                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', tcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]
            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click
                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit:
            if exit == 'menu' and game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                if exit == True:
                    end_game = True

        if error:
            error_text = error
            print("Error detected", error_text)

        if vision and game_state == GameStates.PLAYERS_TURN:
            if vision == 'third eye':
                if interface_skin == 'Tutorial':
                    interface_skin = third_eye('open_eye', color_palette, indoors)
                elif interface_skin == 'Graph':
                    interface_skin = third_eye('close_eye', color_palette, indoors)

            #Recalculate FOV
            fov_recompute = True
            game_state = GameStates.ENEMY_TURN

        if wait and game_state == GameStates.PLAYERS_TURN:
            if game_type == 'viewer':
                entities = game_map.next_map(player, map_type, constants, entities, kolors, current_roster, current_mm)
                fov_map = initialize_fov(game_map)
                fov_recompute = True
                main_con.clear(fg=(0, 0, 0))
            else:
                game_state = GameStates.ENEMY_TURN

        #Process player turn results
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')

            if message:
                message_log.add_message(message)

            if targeting_cancelled:
                game_state = previous_game_state
                message_log.add_message(Message('Targeting cancelled'))

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                targeting_item = targeting
                message_log.add_message(targeting_item.item.targeting_message)

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

        #Enemy turn
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN

#            elif event.type == "MOUSEBUTTONDOWN":
#                mousebuttondown = True

if __name__ == '__main__':
    main()
