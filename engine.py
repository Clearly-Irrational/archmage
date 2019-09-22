import tcod
import tcod.event

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

    #Initialize Player position
    player_x_coord = int(screen_width/2)
    player_y_coord = int(screen_height/2)

    #Create the console
    end_game = False
    while not end_game:
        #Draw the character on the main console
        tcod.console_put_char(main_con, player_x_coord, player_y_coord, '@', tcod.BKGND_NONE)
        #Overlay the main console onto the root console
#        tcod.console_blit(main_con, 0, 0, screen_width, screen_height, 0, 0, 0)
        main_con.blit(dest=root_con)
#        main_con.blit(root_con, 0, 0, screen_width, screen_height, 0, 0, 1.0, 1.0)
#        root_con.print(0, 0, 'Hello World!', (255, 255, 255))
        #Update the console with our changes
        tcod.console_flush()

        #Erase the character so it won't smear on the next update
        tcod.console_put_char(main_con, player_x_coord, player_y_coord, ' ', tcod.BKGND_NONE)       

        #Detect and handle events like key presses or closing the window
        for event in tcod.event.get():
            if event.type == "QUIT":
                end_game = True
            elif event.type == "KEYDOWN":
                keydown = True 
                if event.sym == 97: #a
                    player_x_coord -= 1
                elif event.sym == 100: #d
                    player_x_coord += 1
                elif event.sym == 115: #s
                    player_y_coord += 1
                elif event.sym == 119: #w
                    player_y_coord -= 1
                else:
                    print("Unknown key", event.scancode, event.sym, event.mod, event.repeat)
                    print(event)
#            elif event.type == "MOUSEBUTTONDOWN":
#                mousebuttondown = True

if __name__ == '__main__':
    main()
