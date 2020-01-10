from random import randint, shuffle
from operator import methodcaller

from rectangle import Rect
from tile import Tile
from game_map import GameMap
from fighter import Fighter
from item import Item
from ai import BasicMonster
from entity import Entity
from item_functions import heal
from render_functions import RenderOrder
from generator import gen_monster, roll_monster

#Note, need to replace entities with entities_list to stay consistent

class Dungeon(GameMap):
########################################
#####Generate a traditional dungeon#####
########################################
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_area, max_items_per_area, kolors, current_roster, current_mm):
        rooms = []
        connected_rooms = []
        num_rooms = 0
        tunnel_built = False

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            if num_rooms > 0:
                prev_room = new_room
            new_room = Rect(x, y, w, h)

            # Go through the room list  and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid
                # "paint" it to the map's tiles
                self.create_room(new_room)
 
                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()
 
                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    #connect to the previous room with a tunnel if nearby
                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    #Build a tunnel between rooms
                    dist_threshold = 50
                    tunnel_built = self.build_tunnel(prev_x, prev_y, new_x, new_y, dist_threshold) 
                    #Keep track of connected rooms
                    if tunnel_built == True:
                        if new_room.center() not in connected_rooms:
                            connected_rooms.append(new_room.center())
                        if prev_room.center() not in connected_rooms:
                            connected_rooms.append(prev_room.center())

                #Add monsters
                self.place_entities(new_room, entities, max_monsters_per_area, max_items_per_area, kolors, current_roster, current_mm)
                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        #Add short corridors
        for i in range(0, 30):
            shuffle(rooms)
            first_room = True
            for cur_room in range(0, len(rooms)):
                if first_room == True:
                    first_room = False
                else:
                    (prev_x, prev_y) = rooms[cur_room - 1].center()
                    (cur_x, cur_y) = rooms[cur_room].center()
                    dist_threshold = 25
                    tunnel_built = self.build_tunnel(prev_x, prev_y, cur_x, cur_y, dist_threshold)
                    #Keep track of connected rooms
                    if tunnel_built == True:
                        if rooms[cur_room].center() not in connected_rooms:
                            connected_rooms.append(rooms[cur_room].center())
                        if rooms[cur_room-1].center() not in connected_rooms:
                            connected_rooms.append(rooms[cur_room-1].center())

        #Connect orphan rooms
        for cur_room in range(0, len(rooms)):
            tunnel_built = False
            if rooms[cur_room].center() not in connected_rooms:
                for i in range(0, 1000):
                    rand_room = randint(0, len(rooms) - 1)
                    (rand_x, rand_y) = rooms[rand_room - 1].center()
                    (cur_x, cur_y) = rooms[cur_room].center()
                    dist_threshold = 50
                    tunnel_built = self.build_tunnel(rand_x, rand_y, cur_x, cur_y, dist_threshold)
                    if tunnel_built == True:
                        break

    #Generate a walkable rectangular room
    def create_room(self, room):
        #Go through the tiles in the rectangle and make them passable
        #+1 value ensures adjacent rooms will have a wall between them
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    #Generate a walkable horizontal tunnel
    #x coordinates are not left/right, just represent the ends of a range
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    #Generate a walkable vertical tunnel
    #y coordinates are not up/down, just represent the ends of a range
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    #Combines the tunneling methods available to create a random tunnel
    def build_tunnel(self, prev_x, prev_y, new_x, new_y, dist_threshold):
        diff_x = abs(prev_x - new_x)
        diff_y = abs(prev_y - new_y)
        dist_xy = diff_x + diff_y

        # flip a coin (random number that is either 0 or 1)
        if dist_xy < dist_threshold:
            flip = randint(0, 1)
            if flip == 0:
                # first move horizontally, then vertically
                self.create_h_tunnel(prev_x, new_x, prev_y)
                self.create_v_tunnel(prev_y, new_y, new_x)
            elif flip == 1:
                # first move vertically, then horizontally
                self.create_v_tunnel(prev_y, new_y, prev_x)
                self.create_h_tunnel(prev_x, new_x, new_y)
            return True
        else:
            return False

    def next_map(self, player, map_type, constants, entities, kolors, current_roster, current_mm):
        entities = [player]
        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_room'], constants['max_items_per_room'], kolors, current_roster, current_mm)
        return entities

    def place_entities(self, area, entities, max_monsters_per_area, max_items_per_area, kolors, current_roster, current_mm):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_area)
        number_of_items = randint(0, max_items_per_area)

        for i in range(0, number_of_monsters):
            # Choose a random location in the area
            x = randint(area.x1 + 1, area.x2 - 1)
            y = randint(area.y1 + 1, area.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                #Roll for what monster to populate
                monster_name = roll_monster('dungeon', current_roster)
                #Pull in the dictionary entry for this monster
                m_loader = gen_monster(monster_name, current_mm)
                #Set the monster stats
                fighter_component = Fighter(hp=m_loader['hp'], protection=m_loader['protection'], power=m_loader['power'])
                #Set the ai
                if m_loader['ai_component'] == 'basic':
                    ai_component = BasicMonster()
                #Create the monster entity
                monster = Entity(x, y, m_loader['display_char'], kolors[m_loader['color']], m_loader['display_name'], blocks=True, fighter=fighter_component, render_order=RenderOrder.ACTOR, ai=ai_component)
                #Append the monster to the list of entities
                entities.append(monster)

        for i in range(0, number_of_items):
            # Choose a random location in the area
            x = randint(area.x1 + 1, area.x2 - 1)
            y = randint(area.y1 + 1, area.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                #Create the item entity
                item_component = Item(use_function=heal, amount=4)
                item = Entity(x, y, '!', kolors['potion_violet'], 'Healing Potion', render_order=RenderOrder.ITEM, item=item_component)
                #Append the item to the list of entities
                entities.append(item)
