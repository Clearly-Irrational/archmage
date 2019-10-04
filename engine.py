import tcod
import tcod.event

from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from initialize import get_constants
from game_map import GameMap
from render_functions import clear_all, render_all
from caves import Cave
from dungeons import Dungeon
from world import World

def main():
    #Set the initial variables
    constants = get_constants()

    #Set the font file and settings
    font_file = 'font_arial10x10.png'
    tcod.console_set_custom_font(font_file, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_map_ascii_codes_to_font(256, 32, 0, 1)  #map all characters in 2nd row
    tcod.console_map_ascii_codes_to_font(256+32, 32, 0, 2)  #map all characters in 3rd row

    #Create the screen, the root console
    root_con = tcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['screen_title'], constants['screen_fullscreen'], constants['screen_renderer'], constants['screen_order'], constants['screen_vsync'])

    #Create another console where we'll draw before overlaying it on the root
    main_con = tcod.console.Console(constants['screen_width'], constants['screen_height'], constants['screen_order'])

    #Initialize entities
    player = Entity(int(constants['screen_width']/2), int(constants['screen_height']/2), '@', tcod.black)
    npc = Entity(int(constants['screen_width'] / 2 - 5), int(constants['screen_height'] / 2), '@', tcod.yellow)
    entities = [player, npc]

    #Initialize the map
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    interface_skin = 'Tutorial' #Choices: Graph, Tutorial

    if interface_skin == 'Graph':
        colors = {
            #steelblue (70, 130, 180)
            'dark_wall': tcod.Color(70, 130, 180),
            'dark_ground': tcod.Color(70, 130, 180),
            'light_wall': tcod.Color(130, 110, 50),
            'light_ground': tcod.Color(200, 180, 50),
            'purple_fill': tcod.Color(128, 0, 128),
            'console_white': tcod.Color(255, 255, 255)
        }
    elif interface_skin == 'Tutorial':
        colors = {
            'dark_wall': tcod.Color(0, 0, 100),
            'dark_ground': tcod.Color(50, 50, 150),
            'light_wall': tcod.Color(130, 110, 50),
            'light_ground': tcod.Color(200, 180, 50),
            'purple_fill': tcod.Color(128, 0, 128),
            'console_white': tcod.Color(255, 255, 255),
            'light_water_blue': tcod.Color(0, 0, 255),
            'light_plains_brown': tcod.Color(127, 101, 63),
            'light_forest_green': tcod.Color(0, 255, 0),
            'light_mountain_grey': tcod.Color(127, 127, 127),
            'dark_water_blue': tcod.Color(0, 0, 191),
            'dark_plains_brown': tcod.Color(94, 75, 47),
            'dark_forest_green': tcod.Color(0, 191, 0),
            'dark_mountain_grey': tcod.Color(95, 95, 95)
        }

    map_type = 'Cave' #Choices: Dungeon, Cave, World

    if map_type == 'Dungeon':
        indoors = True
        game_map = Dungeon(constants['map_width'], constants['map_height'])
        game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player)
    elif map_type == 'Cave':
        indoors = True
        game_map = Cave(constants['map_width'], constants['map_height'])
        game_map.make_cave(constants['map_width'], constants['map_height'], player)
    elif map_type == 'World':
        indoors = False
        game_map = World(constants['map_width'], constants['map_height'])
        game_map.make_world(constants['map_width'], constants['map_height'], player)

    #Initialize FOV and calculate on start
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    game_type = 'normal' #choices normal, viewer

    #Initialize main loop
    end_game = False
    while not end_game:
        #Recomput FOV if necessary
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        #Render all entities & tiles on main console and blit them to the root console
        render_all(main_con, root_con, entities, game_map, fov_map, fov_recompute, constants['screen_width'], constants['screen_height'], colors, game_type, interface_skin, indoors)
        #Reset FOV check
        fov_recompute = False
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
        wait = action.get('wait')

        if move:
            dx, dy = move
            #If nothing is blocking then move the player
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
            #Recalculate FOV if player moves
            fov_recompute = True

        if exit:
            end_game = True

        if error:
            error_text = error
            print("Error detected", error_text)

        if wait:
            if game_type == 'viewer':
                entities = game_map.next_map(player, map_type, constants)
                fov_map = initialize_fov(game_map)
                fov_recompute = True
                main_con.clear()

#            elif event.type == "MOUSEBUTTONDOWN":
#                mousebuttondown = True

if __name__ == '__main__':
    main()
