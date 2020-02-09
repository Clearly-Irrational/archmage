import tcod

from fighter import Fighter
from inventory import Inventory
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from render_functions import RenderOrder
from game_map import GameMap
from caves import Cave
from dungeons import Dungeon
from world import World

def get_constants():
    #Screen
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

    #Fonts
    font_file = 'fonts/font_arial12x12.png' 

    #Map
    map_width = screen_width
    map_height = screen_height - panel_height
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

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
        'font_file': font_file,
        'map_width': map_width,
        'map_height': map_height,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
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

def get_game_variables(constants, kolors, current_roster, current_mm):
    fighter_component = Fighter(hp=30, protection=2, power=5)
    inventory_component = Inventory(26)
    player = Entity(0, 0, '@', tcod.black, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component)
    entities = [player]

    map_type = 'Dungeon' #Choices: Dungeon, Cave, World

    if map_type == 'Dungeon':
        indoors = True
        game_map = Dungeon(constants['map_width'], constants['map_height'])
        game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_room'], constants['max_items_per_room'], kolors, current_roster, current_mm)
    elif map_type == 'Cave':
        indoors = True
        game_map = Cave(constants['map_width'], constants['map_height'])
        game_map.make_cave(constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_cave'], constants['max_items_per_cave'], kolors, current_roster, current_mm)
    elif map_type == 'World':
        indoors = False
        game_map = World(constants['map_width'], constants['map_height'])
        game_map.make_world(constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_spawn'], kolors, current_roster, current_mm)

    #Initialize the message log
    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, indoors, message_log, game_state
