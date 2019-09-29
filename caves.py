from random import randint

from tile import Tile
from game_map import GameMap

class Cave(GameMap):
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

    def next_map(self, player, map_type, constants):
        entities = [player]
        self.tiles = self.initialize_tiles()
        self.make_cave(constants['map_width'], constants['map_height'], player)
        return entities
