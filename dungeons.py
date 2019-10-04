from random import randint
from operator import methodcaller

from rectangle import Rect
from tile import Tile
from game_map import GameMap

class Dungeon(GameMap):
########################################
#####Generate a traditional dungeon#####
########################################
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
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
                    #Sometimes connect it to the previous room with a tunnel
                    if randint(0, 2) == 2:
                        # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()
                        #Build a tunnel between rooms
                        self.build_tunnel(prev_x, prev_y, new_x, new_y) 

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        rooms.sort(key=methodcaller('center'))
        first_room = True
        for cur_room in range(0, len(rooms)):
            if first_room == True:
                first_room = False
            else:
                (prev_x, prev_y) = rooms[cur_room - 1].center()
                (cur_x, cur_y) = rooms[cur_room].center()

                if randint(0, 2) == 2:
                    self.build_tunnel(prev_x, prev_y, cur_x, cur_y)

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
    def build_tunnel(self, prev_x, prev_y, new_x, new_y):
        mid_x = int(new_x / 2)
        mid_y = int(new_x / 2)
        # flip a coin (random number that is either 0 or 1)
        flip = randint(0, 2)
        if flip == 0:
            # first move horizontally, then vertically
            self.create_h_tunnel(prev_x, new_x, prev_y)
            self.create_v_tunnel(prev_y, new_y, new_x)
        elif flip == 1:
            # first move vertically, then horizontally
            self.create_v_tunnel(prev_y, new_y, prev_x)
            self.create_h_tunnel(prev_x, new_x, new_y)
        elif flip == 2:
            flip2 = randint(0, 2)
            if flip2 == 0:
                #Double bend tunnel, horizontal first
                self.create_h_tunnel(prev_x, mid_x, prev_y)
                self.create_v_tunnel(prev_y, mid_y, mid_x)
                self.create_h_tunnel(mid_x, new_x, mid_y)
                self.create_v_tunnel(mid_y, new_y, new_x)
            elif flip2 == 1:
                #Double bend tunnel, vertical first
                self.create_v_tunnel(prev_y, mid_y, prev_x)
                self.create_h_tunnel(prev_x, mid_x, mid_y)
                self.create_v_tunnel(mid_y, new_y, mid_x)
                self.create_h_tunnel(mid_x, new_x, new_y)
            else:
                #Creates a possible dead end
                mid_x = int(mid_x / 2)
                mid_y = int(mid_y /2)
                flip3 = randint(0, 2)
                if flip3 == 0:
                    self.create_h_tunnel(prev_x, mid_x, prev_y)
                elif flip3 == 1:
                    self.create_v_tunnel(prev_y, mid_y, mid_x)
                else:
                    new_x = int(new_x / 2)
                    new_y = int(new_y / 2)
                    flip4 = randint(0, 1)
                    if flip4 == 0:
                        self.create_h_tunnel(prev_x, mid_x, prev_y)
                        self.create_v_tunnel(mid_y, new_y, new_x)
                    else: 
                        self.create_v_tunnel(mid_y, new_y, new_x)
                        self.create_h_tunnel(prev_x, mid_x, prev_y)

    def next_map(self, player, map_type, constants):
        entities = [player]
        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player)
        return entities