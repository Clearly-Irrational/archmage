import tcod

def get_constants():
    screen_width = 136 #Default 80
    screen_height = 82 #Default 50
    screen_title = 'Archmage - The True Path'
    screen_fullscreen = False
    screen_renderer = tcod.RENDERER_SDL2
    screen_order = 'F'
    screen_vsync = True

    #Panel
    hp_bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height
    message_x = hp_bar_width + 2
    message_width = screen_width - hp_bar_width - 2
    message_height = panel_height - 1

    #Map
    map_width = screen_width
    map_height = screen_height - panel_height

    #Dungeons
    room_max_size = 16
    room_min_size = 4
    max_rooms = 180
    max_monsters_per_room = 3
    max_items_per_room = 2

    #Caves
    max_monsters_per_cave = 5
    max_items_per_cave = 3

    #World
    max_monsters_per_spawn = 8

    constants = {
        'screen_width': screen_width,
        'screen_height': screen_height,
        'screen_title': screen_title,
        'screen_fullscreen': screen_fullscreen,
        'screen_renderer': screen_renderer,
        'screen_order': screen_order,
        'screen_vsync': screen_vsync,
        'hp_bar_width': hp_bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'max_monsters_per_room': max_monsters_per_room,
        'max_monsters_per_cave': max_monsters_per_cave,
        'max_monsters_per_spawn': max_monsters_per_spawn,
        'max_items_per_room': max_items_per_room,
        'max_items_per_cave': max_items_per_cave
    }

    return constants
