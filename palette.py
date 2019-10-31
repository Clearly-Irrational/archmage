from tcod import Color

class Palette:
    def __init__(self):
        self.colors = {
            #indoors
            'dark_wall': Color(0, 0, 100),
            'dark_ground': Color(50, 50, 150),
            'light_wall': Color(130, 110, 50),
            'light_ground': Color(200, 180, 50),
            'purple_fill': Color(128, 0, 128),
            #outdoors
            'light_water': Color(0, 0, 255), #Blue
            'light_shallows': Color(100, 100, 255), #Blue
            'light_sand': Color(255, 232, 165), #Amber
            'light_plains': Color(0, 255, 0), #Green
            'light_hills': Color(127, 101, 63), #Brown
            'light_mountain': Color(127, 127, 127), #Grey
            'light_snow': Color(255, 255, 255), #White
            'dark_water': Color(0, 0, 191), #Blue
            'dark_shallows': Color(63, 63, 255), #Blue
            'dark_sand': Color(255, 219, 114), #Amber
            'dark_plains': Color(0, 191, 0), #Green
            'dark_hills': Color(94, 75, 47), #Brown
            'dark_mountain': Color(95, 95, 95), #Grey
            'dark_snow': Color(223, 223, 223), #White
            'tree_green': Color(0, 63, 0), #Green
            #Entities
            'console_white': Color(255, 255, 255),
            'ape_c_white': Color(230, 230, 230),
            'orc_green': Color(63, 127, 63),
            'troll_green': Color(0, 127, 0),
            'spider_brown': Color(31, 24, 15),
            'skeleton_white': Color(230, 230, 230),
            'zombie_black': Color(0, 0, 0),
            'ghoul_green': Color(63, 127, 63),
            'banshee_blue': Color(0, 0, 127),
            'potion_violet': Color(127, 0, 255)
        }

    def get_colors(self):
        return self.colors 

    def set_color(self, key, red, green, blue):
        self.colors[key] = Color(red, green, blue)
