from random import randint

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
