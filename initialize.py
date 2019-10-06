import tcod

def get_constants():
    screen_width = 160 #Default 80
    screen_height = 100 #Default 50
    screen_title = 'Archmage - The True Path'
    screen_fullscreen = False
    screen_renderer = tcod.RENDERER_SDL2
    screen_order = 'F'
    screen_vsync = True

    map_width = screen_width
    map_height = screen_height - 5
    room_max_size = 16
    room_min_size = 4
    max_rooms = 180
    max_monsters_per_room = 3

    constants = {
        'screen_width': screen_width,
        'screen_height': screen_height,
        'screen_title': screen_title,
        'screen_fullscreen': screen_fullscreen,
        'screen_renderer': screen_renderer,
        'screen_order': screen_order,
        'screen_vsync': screen_vsync,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'max_monsters_per_room': max_monsters_per_room
    }

    return constants
