import pygame
import snake_rules

class MapReader:
    def __init__(self, f_path):
        
        with open(f_path) as f:
            self.contents = f.readlines()
        
        self.res = self.set_resolution()
        

    def get_wall_positions(self):
        wall_objects = []
        for y in range(len(self.contents)):
            for x in range(len(self.contents[y])):
                if self.contents[y][x] == "x":
                    wall_objects.append(((x + 1)* snake_rules.pixel_size[0], (y + 1) * snake_rules.pixel_size[1]))
        return wall_objects

    def set_resolution(self):

        largest_string_length = 0

        for line in self.contents:
            if len(line) > largest_string_length:
                largest_string_length = len(line)

        x = (largest_string_length + 1) * snake_rules.pixel_size[0]
        y = (len(self.contents) + 2) * snake_rules.pixel_size[1]

        return (x, y)


        
    