import pygame
import snake_rules
import random

class MapReader:
    def __init__(self, f_path, right = 1, down = 1):
        
        with open(f_path) as f:
            self.contents = f.readlines()
        
        self.res = self.set_resolution()
        self.map_representation = {}
        self.right = right
        self.down = down
        self.spawn_area =  self.get_map_pixels()
        
    def get_wall_positions(self):
        wall_objects = []
        for y in range(len(self.contents)):
            for x in range(len(self.contents[y])):
                if self.contents[y][x] == "x":
                    wall_objects.append(((x + 1) * snake_rules.pixel_size[0], (y + 1) * snake_rules.pixel_size[1]))
        return wall_objects

    def get_random_spawn_location(self):
        x = random.randint(self.spawn_area[0][0], self.spawn_area[0][1])
        y = random.randint(self.spawn_area[1][0], self.spawn_area[1][1])

        return (x *  snake_rules.pixel_size[0], y * snake_rules.pixel_size[1])

    def get_map_pixels(self):
        largest_string_length = 0
        for line in self.contents:
            if len(line) > largest_string_length:
                largest_string_length = len(line)

        x = largest_string_length
        y = len(self.contents)

        return (self.right, x), (self.down, y)


    def set_resolution(self):

        largest_string_length = 0

        for line in self.contents:
            if len(line) > largest_string_length:
                largest_string_length = len(line)

        x = (largest_string_length + 1) * snake_rules.pixel_size[0]
        y = (len(self.contents) + 2) * snake_rules.pixel_size[1]

        return (x, y)


        
    