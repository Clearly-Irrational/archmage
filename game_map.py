import tcod #remove later and abstract monster colors
from random import randint

from initialize import get_constants
from tile import Tile
from entity import Entity

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

    def place_entities(self, area, entities, max_monsters_per_area):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_area)

        for i in range(0, number_of_monsters):
            # Choose a random location in the area
            x = randint(area.x1 + 1, area.x2 - 1)
            y = randint(area.y1 + 1, area.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', blocks=True)
                else:
                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', blocks=True)

                entities.append(monster)

#    def next_map(self, player, map_type):
#        entities = [player]
#        self.tiles = self.initialize_tiles()
#
#        return entities
