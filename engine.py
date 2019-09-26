import tcod
import tcod.event

from entity import Entity
from input_handlers import handle_keys
from game_map import GameMap
from render_functions import clear_all, render_all

def main():
    #Set the screen variables
    screen_width = 80
    screen_height = 50
    screen_title = 'archmage alpha'
    screen_fullscreen = False
    screen_renderer = tcod.RENDERER_SDL2
    screen_order = 'F'
    screen_vsync = True

    #Set the font file and settings
    font_file = 'font_arial10x10.png'
    tcod.console_set_custom_font(font_file, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    #Create the screen, the root console
    root_con = tcod.console_init_root(screen_width, screen_height, screen_title, screen_fullscreen, screen_renderer, screen_order, screen_vsync)

    #Create another console where we'll draw before overlaying it on the root
    main_con = tcod.console.Console(screen_width, screen_height, screen_order)

    #Initialize entities
    player = Entity(int(screen_width/2), int(screen_height/2), '@', tcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', tcod.yellow)
    entities = [player, npc]

    #Initialize the map
    map_width = screen_width
    map_height = screen_height - 5

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150)
    }

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)
#    game_map.make_cave(map_width, map_height, player)

    #Initialize main loop
    end_game = False
    while not end_game:
        #Render all entities & tiles on main console and blit them to the root console
        render_all(main_con, root_con, entities, game_map, screen_width, screen_height, colors)
        #Update the console with our changes
        tcod.console_flush()
        #Erase all entities on main console so they won't smear on next update
        clear_all(main_con, entities)

        #initialize loop variables
        action = {'none': True}

        #Detect and handle events
        for event in tcod.event.get():
            if event.type == "QUIT": #Window was closed
                action = {'exit': True}
            elif event.type == "KEYDOWN": #A key was depressed
                action = handle_keys(event)

        move = action.get('move')
        exit = action.get('exit')
        error = action.get('error')

        if move:
            dx, dy = move
            #If nothing is blocking then move the player
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if exit:
            end_game = True

        if error:
            error_text = error
            print("Error detected", error_text)

#            elif event.type == "MOUSEBUTTONDOWN":
#                mousebuttondown = True

if __name__ == '__main__':
    main()
