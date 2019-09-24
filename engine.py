import tcod
import tcod.event

from entity import Entity
from input_handlers import handle_keys
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

    #Initialize main loop
    end_game = False
    while not end_game:
        #Render all entities on main console and blit them to the root console
        render_all(main_con, root_con, entities, screen_width, screen_height)
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
