import tcod

def handle_keys(event):
    keypress = event.sym
    #Movement keys
    if keypress == 119: #w move up
        return {'move': (0, -1)}
    elif keypress == 115: #s move down
        return {'move': (0, 1)}
    elif keypress == 97: #a move left
        return {'move': (-1, 0)}
    elif keypress == 100: #d move right
        return {'move': (1, 0)}
    else:
#        print("Unknown key", "Scancode=", event.scancode, "Symbol=", event.sym, "Mod=", event.mod, "Repeat=", event.repeat)
#        print(event)
        return {'Unknown_Key': True}
    #Somehow we got here even though no key was pressed
    return {'error': "handle_keys - no key pressed"}
