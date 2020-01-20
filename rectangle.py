class Rect:
    #Defines a rectangular room
    def __init__(self, x, y, width, height):
        #Top left coordinates
        self.x1 = x 
        self.y1 = y
        #Bottm right coordinates
        self.x2 = x + width
        self.y2 = y + height
        #Properties
        self.room_type = "rectangle"

    #Calculates the center of the rectangle, decimals truncated
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    # returns true if this rectangle intersects with another one
    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    #Find the edges of the room
    def edge(self):
        edge_list = []
        for x in range(self.x1, self.x2+1):
            for y in range(self.y1, self.y2+1):
                if (x == self.x1) or (x == self.x2+1) or (y == self.y1) or (y == self.y2+1):
                    cur_coord = (x, y)
                if cur_coord not in edge_list:
                    edge_list.append(cur_coord)
        return edge_list 
