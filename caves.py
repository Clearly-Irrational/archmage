import tcod #remove later and abstract monster colors
from random import randint
import random
from math import sqrt

from tile import Tile
from game_map import GameMap
from entity import Entity

class Cave(GameMap):
##################################################
#####Generate a cellular automata cave system#####
##################################################
#Credit to Michael Cook and his blog post Generate Random Cave Levels Using Cellular Automata
#Credit to https://github.com/AtTheMatinee/dungeon-generation whose implmentation of Andy Stobirski's method I cribbed shamelessly
#This method will generate levels that are cavey looking and mostly connected, full connection was actually not desired by design
    caves = []
    checked = []
    cave_min_size = 1 #Size in tiles

    def make_cave(self, map_width, map_height, player, entities, max_monsters_per_area):
        #Generator variables
        #40, 5, 5, 5 works passably
        initialy_open_chance = 40
        number_of_extra_passes = 5
        wall_create_threshold = 5
        wall_remove_threshold = 5

        #First pass
        for y in range(1, map_height-1):
            for x in range(1, map_width-1):
                if randint(1, 100) <= initialy_open_chance:
                    self.tiles[x][y].blocked = False
                    self.tiles[x][y].block_sight = False
        for loop in range(0, number_of_extra_passes):
            self.next_pass(map_width, map_height, wall_create_threshold, wall_remove_threshold)

        #Creates empty 2D array or clears existing array
        self.checked = [[0
            for y in range(0, map_height)]
                for x in range(0, map_width)]

        self.get_caves(map_width, map_height)
#        print("# of Caves:", len(self.caves))
        self.connect_caves(map_width, map_height)
        self.cleanup_map(map_width, map_height)

        #Place the player
        placed = False
        while not placed:
            rand_x = randint(1, map_width - 1)
            rand_y = randint(1, map_height - 1)
            if self.tiles[rand_x][rand_y].blocked == False:
                player.x = rand_x
                player.y = rand_y
                placed = True

        #Add monsters
        for cur_cave in self.caves:
            self.place_entities(cur_cave, entities, max_monsters_per_area)

    #Next pass
    def next_pass(self, map_width, map_height, wall_create_threshold, wall_remove_threshold):
        next_pass = self
        for y in range(1, map_height-1):
            for x in range(1, map_width-1):
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

    def next_map(self, player, map_type, constants, entities):
        entities = [player]
        self.tiles = self.initialize_tiles()
        self.make_cave(constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_cave'])
        return entities

    def get_caves(self, map_width, map_height):
        #Locate all the caves and store them
        for x in range(0, map_width):
            for y in range(0, map_height):
                if self.checked[x][y] == 0:
                    self.flood_fill(x,y)
        #Rest checks so that we can do connectivity tests when tunneling
        for set in self.caves:
            for cur_tile in set:
                self.checked[cur_tile[0]][cur_tile[1]] = 0 

    def flood_fill(self,x,y):
        cave = set() #Create a set, will contain all tiles in this cave
        cur_tile = (x,y) #x,y coordinates of current tile
        to_fill = set([cur_tile]) #Add the current tile to the set of tiles to be filled
        wall = self.tiles[x][y].blocked
        while to_fill: #While there are tiles to be filled in the set
            cur_tile = to_fill.pop() #grab the last tile in the set

            if cur_tile not in cave and not wall: #If this tile is open and isn't part of the cave
                cave.add(cur_tile) #Add the tile to the cave set
                x = cur_tile[0]
                y = cur_tile[1]

                self.checked[x][y] = 1
                #Uncomment to turn floodfilled tiles purple
                #self.tiles[x][y].floodfilled = True

                #Define adjacent cells
                north = (x,y-1)
                south = (x,y+1)
                east = (x+1,y)
                west = (x-1,y)

                #Check adjacent cells
                for direction in [north,south,east,west]:
                    if self.checked[direction[0]][direction[1]] == 0 and not self.tiles[direction[0]][direction[1]].blocked:
                        if direction not in to_fill and direction not in cave:
                            to_fill.add(direction)

        if len(cave) >= self.cave_min_size:
            self.caves.append(cave)

    def connect_caves(self, map_width, map_height):
        for loop in range(0,2):
            #Find the closest cave to the current cave
            for cur_cave in self.caves:
                for point1 in cur_cave: break #Get an element from cave1
                point2 = False
                distance = False
                for next_cave in self.caves:
                    if next_cave != cur_cave and not self.check_connected(cur_cave, next_cave):
                        #Choose a random point from next cave
                        for next_point in next_cave: break #Get an element from cave2
                        #Compare distance of point1 to old and new point2
                        new_distance = self.distance_check(point1, next_point)
                        if (new_distance < distance) or distance == False:
                            point2 = next_point
                            distance = new_distance
                if point2: #If all tunnels are connected, point2 == False
                    self.create_tunnel(point1, point2, cur_cave, map_width, map_height)

    def check_connected(self, cave1, cave2):
        #Floods cave1, then checks a point in cave2 for the flood
        connected_region = set()
        for start in cave1: break #Get an element from cave1

        to_fill = set([start])
        while to_fill:
            cur_tile = to_fill.pop()

            if cur_tile not in connected_region:
                connected_region.add(cur_tile)
                x = cur_tile[0]
                y = cur_tile[1]

                self.checked[x][y] = 1
                #Uncomment to turn floodfilled tiles purple
                #self.tiles[x][y].floodfilled = True

                #Define adjacent cells
                north = (x,y-1)
                south = (x,y+1)
                east = (x+1,y)
                west = (x-1,y)

                for direction in [north, south, east, west]:
                    if self.checked[direction[0]][direction[1]] == 0 and not self.tiles[direction[0]][direction[1]].blocked:
                        if direction not in to_fill and direction not in connected_region:
                            to_fill.add(direction)

        for end in cave2: break #Get an element from cave2
        if end in connected_region: return True
        else: return False

    def distance_check(self, point1, point2):
        d = sqrt( (point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
        return d

    def create_tunnel(self, point1, point2, cur_cave, map_width, map_height):
        #Run a heavily weighted random walk from point2 to point1
        drunk_x = point2[0]
        drunk_y = point2[1]
        while(drunk_x, drunk_y) not in cur_cave:
            #Choose Direction
            north = 1.0
            south = 1.0
            east = 1.0
            west = 1.0

            weight = 1

            # weight the random walk against edges
            if drunk_x < point1[0]: # drunkard is left of point1
                east += weight
            elif drunk_x > point1[0]: # drunkard is right of point1
                west += weight
            if drunk_y < point1[1]: # drunkard is above point1
                south += weight
            elif drunk_y > point1[1]: # drunkard is below point1
                north += weight

            # normalize probabilities so they form a range from 0 to 1
            total = north+south+east+west
            north /= total
            south /= total
            east /= total
            west /= total

            # choose the direction
            choice = random.random()
            if 0 <= choice < north:
                dx = 0
                dy = -1
            elif north <= choice < (north+south):
                dx = 0
                dy = 1
            elif (north+south) <= choice < (north+south+east):
                dx = 1
                dy = 0
            else:
                dx = -1
                dy = 0

            # ==== Walk ====
            #Check colision at edges
            if (0 < drunk_x+dx < map_width-1) and (0 < drunk_y+dy < map_height-1):
                drunk_x += dx
                drunk_y += dy
                if self.tiles[drunk_x][drunk_y].blocked:
                    self.tiles[drunk_x][drunk_y].blocked = False
                    self.tiles[drunk_x][drunk_y].block_sight = False

    def cleanup_map(self,map_width,map_height):
        smoothing = 1
        for i in range (0,1):
            # Look at each cell individually and check for smoothness
            for x in range(1,map_width-1):
                for y in range (1,map_height-1):
                    if (self.tiles[x][y].blocked) and (self.get_walls_simple(x,y) <= smoothing):
                        self.tiles[x][y].blocked = False
                        self.tiles[x][y].block_sight = False

    def get_walls_simple(self, x, y): # finds the walls in four directions
        wall_counter = 0
        if (self.tiles[x][y-1].blocked): # Check north
            wall_counter += 1
        if (self.tiles[x][y+1].blocked): # Check south
            wall_counter += 1
        if (self.tiles[x-1][y].blocked): # Check west
            wall_counter += 1
        if (self.tiles[x+1][y].blocked): # Check east
            wall_counter += 1

        return wall_counter

    def place_entities(self, area, entities, max_monsters_per_area):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_area)
            
        for i in range(0, number_of_monsters):
            for coord in area: break #Get an element from area
            (x, y) = coord

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', blocks=True)
                else:
                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', blocks=True)

                entities.append(monster)

