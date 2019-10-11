from random import randint
import random
import tcod
import noise
from PIL import Image  #Actually imports from pillow

from tile import Tile
from game_map import GameMap

class World(GameMap):
##############################
#####Generate a world map#####
##############################


    def make_world(self, map_width, map_height, player, entities, max_monsters_per_spawn, kolors):
        #elevation = randint(0, 3) #low, level, moderate, high
        #moisture = randint(0, 2) #dry, normal, water
        #temperature = randing(0, 2) #cold, normal, hot
        #vegetation = randint(0, 2) #none, grass, woods
        scale = 100.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        seed_h = randint(0, 131072)
        seed_v = randint(0, 131072)

        water_threshold = -0.25
        shallows_threshold = -0.2
        sand_threshold = -0.1775
        plains_threshold = 0.1
        hills_threshold = 0.3
        mountain_threshold = 0.425
        vegetation_threshold = -0.05

        world_height = [[0
            for y in range(0, map_height)]
                for x in range(0, map_width)]

        world_vegetation = [[0
            for y in range(0, map_height)]
                for x in range(0, map_width)]

        for y in range(0, map_height):
            for x in range(0, map_width):
                #Height map
                world_height[x][y] = noise.snoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=map_width, repeaty=map_height, base=seed_h)
                if world_height[x][y] < water_threshold:
                    self.tiles[x][y].terrain = 0 #Water
                elif world_height[x][y] < shallows_threshold:
                    self.tiles[x][y].terrain = 1 #Shallows
                elif world_height[x][y] < sand_threshold:
                    self.tiles[x][y].terrain = 2 #Sand
                elif world_height[x][y] < plains_threshold:
                    self.tiles[x][y].terrain = 3 #Plains
                elif world_height[x][y] < hills_threshold:
                    self.tiles[x][y].terrain = 4 #Hills
                elif world_height[x][y] < mountain_threshold:
                    self.tiles[x][y].terrain = 5 #Mountains
                else:
                    self.tiles[x][y].terrain = 6 #Snow
                #Vegetation map
                world_vegetation[x][y] = noise.snoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=map_width, repeaty=map_height, base=seed_v)
                if world_vegetation[x][y] < vegetation_threshold:
                    self.tiles[x][y].vegetation = 1 #Yes
                else:
                    self.tiles[x][y].vegetation = 0 #None
                #Tile settings
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
#                if world_height[x][y] < -0.2:
#                    print(world_height[x][y])
 
    def next_map(self, player, map_type, constants, entities, kolors):
        entities = [player]
        self.tiles = self.initialize_tiles()
        self.make_world(constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_spawn'], kolors)
        return entities
