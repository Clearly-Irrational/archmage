from random import randint

from rectangle import Rect
from tile import Tile

class GameMap:
    #Initialize the map data
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    #Define the tile states
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    #Determine if a tile is blocked
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

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
                    # connect it to the previous room with a tunnel
 
                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
 
                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
 
                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

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

##################################################
#####Generate a cellular automata cave system#####
##################################################
    def make_cave(self, map_width, map_height, player):
        #Generator variables
        #40, 5, 5, 5 works passably
        initialy_open_chance = 40
        number_of_extra_passes = 5
        wall_create_threshold = 5
        wall_remove_threshold = 5

        #First pass
        for y in range(0, map_height):
            for x in range(0, map_width):
                if randint(1, 100) <= initialy_open_chance:
                    self.tiles[x][y].blocked = False
                    self.tiles[x][y].block_sight = False
        for loop in range(0, number_of_extra_passes):
            self.next_pass(map_width, map_height, wall_create_threshold, wall_remove_threshold)

        #Place the player
        placed = False
        while not placed:
            rand_x = randint(0, map_width - 1)
            rand_y = randint(0, map_height - 1)
            if self.tiles[rand_x][rand_y].blocked == False:
                player.x = rand_x
                player.y = rand_y
                placed = True

    #Next pass
    def next_pass(self, map_width, map_height, wall_create_threshold, wall_remove_threshold):
        next_pass = self
        for y in range(0, map_height):
            for x in range(0, map_width):
                wall_count = 0
                top_limit = 0 if y == 0 else 1
                bottom_limit = 1 if y == map_height - 1 else 2
                left_limit = 0 if x == 0 else 1
                right_limit = 1 if x == map_width - 1 else 2
                for y2 in range(y-top_limit, y+bottom_limit): #Note Range max is -1 by default
                    for x2 in range(x-left_limit, x+right_limit):
                        if self.tiles[x2][y2].blocked == True:
                            wall_count += 1
                if wall_count > wall_create_threshold:
                    next_pass.tiles[x][y].blocked = True
                    next_pass.tiles[x][y].block_sight = True
                elif wall_count < wall_remove_threshold:
                    next_pass.tiles[x][y].blocked = False
                    next_pass.tiles[x][y].block_sight = False
        self = next_pass
