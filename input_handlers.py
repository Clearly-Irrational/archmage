import tcod

from game_states import GameStates

def handle_keys(event, mod_key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(event, mod_key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(event, mod_key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(event, mod_key)

    return {}

def handle_player_turn_keys(event, mod_key):
    keypress = event.sym

    #Action keys
    if mod_key == 'l_shift':
        if keypress == 119: #W move up and left
            return {'move': (-1, -1)}
        elif keypress == 115: #S move down and right
            return {'move': (1, 1)}
        elif keypress == 97: #A move left and down
            return {'move': (-1, 1)}
        elif keypress == 100: #D move right and up
            return {'move': (1, -1)}
        elif keypress == 103: #G get rid of item
            return {'drop_inventory': True}
        return {'Unknown_Key': True}
    else:
        if keypress == 119: #w move up
            return {'move': (0, -1)}
        elif keypress == 115: #s move down
            return {'move': (0, 1)}
        elif keypress == 97: #a move left
            return {'move': (-1, 0)}
        elif keypress == 100: #d move right
            return {'move': (1, 0)}
        elif keypress == 116: #t third eye mode
            return {'vision': 'third eye'}
        elif keypress == 103: #g grab an item
            return {'pickup': True}
        elif keypress == 105: #i inventory
            return {'show_inventory': True}
        elif keypress == 32: #space wait or generate new map in viewer mode
            return {'wait': True}
        elif keypress == 27: #esc exit
            return {'exit': 'menu'}
        else:
            print("Unknown key", "Scancode=", event.scancode, "Symbol=", event.sym, "Mod=", event.mod, "Repeat=", event.repeat)
            print(event)
            return {'Unknown_Key': True}
        #Somehow we got here even though no key was pressed
        return {'error': "handle_keys - no key pressed"}

def handle_player_dead_keys(event, mod_key):
    keypress = event.sym

    if keypress == 105: #i inventory
        return {'show_inventory': True}
    elif keypress == 27: #esc exit
        return {'exit': 'menu'}

    return {}

def handle_inventory_keys(event, mod_key):
    keypress = event.sym
    index = keypress - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if keypress == 27: #esc exit
        return {'exit': 'menu'}

    return {} 
