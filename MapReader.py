import pygame
import snake_rules
import random

class MapReader:
    def __init__(self, f_path, right = 1, down = 1):
        
        with open(f_path) as f:
            self.contents = f.readlines()
        
        self.res = self.set_resolution()
        self.map_border = []
        self.map_representation = {}
        self.right = right
        self.down = down
        self.spawn_area =  self.get_map_pixels()
        self.map_representation = self.set_wall_positions()
        
    def set_wall_positions(self):
        wall_objects = []
        for y in range(len(self.contents)):

            for x in range(len(self.contents[y])):
                if self.contents[y][x] == "x":
                    wall_objects.append(((x + 1) * snake_rules.pixel_size[0], (y + 1) * snake_rules.pixel_size[1]))
        return wall_objects

    def get_wall_positions(self):
        return self.map_representation

    def get_random_spawn_location(self):
        
        x = random.randint(self.spawn_area[0][0], self.spawn_area[0][1]) * snake_rules.pixel_size[0]
        y = random.randint(self.spawn_area[1][0], self.spawn_area[1][1]) * snake_rules.pixel_size[1]
        
        while (self.is_outside_map_border((x,y))):
            x = random.randint(self.spawn_area[0][0], self.spawn_area[0][1]) * snake_rules.pixel_size[0]
            y = random.randint(self.spawn_area[1][0], self.spawn_area[1][1]) * snake_rules.pixel_size[1]

        return (x,y)


            
    def outside_y(self, pos):
        column = self.get_column(pos[0])
        if pos[1] > self.find_largest_y_on_column(column) or pos[1] < self.find_smallest_y_on_column(column):
            return True
        return False
    
    def outside_x(self, pos):
        row = self.get_row(pos[1])
        if pos[0] > self.find_largest_x_on_row(row) or pos[0] < self.find_smallest_x_on_row(row):
            return True
        return False


    def find_smallest_y_on_column(self,column):
        smallest_y = 2000
        for pos in column:
            if pos[1] < smallest_y:
                smallest_y = pos[1]

        return smallest_y

    def find_smallest_x_on_row(self,row):
        smallest_x = 2000
        for pos in row:
            if pos[0] < smallest_x:
                smallest_x = pos[0]

        return smallest_x

    def find_largest_x_on_row(self,row):
        largest_x = -2000
        for pos in row:
            if pos[0] > largest_x:
                largest_x = pos[0]

        return largest_x
    
        

    def find_largest_y_on_column(self, column):
        largest_y = -2000
        for pos in column:
            if pos[1] > largest_y:
                largest_y = pos[1]
        return largest_y

        
    def get_column(self, x):
        column = []
        for pos in self.map_representation:
            if pos[0] == x:
                column.append(pos)
        return column

    def get_row(self, y):
        row = []
        for pos in self.map_representation:
            if pos[1] == y:
                row.append(pos)
        return row


    def border_y(self, x, y):
    
        y_pos_on_column = self.on_column(x)
        
        if self.smallest_y_on_column(y, y_pos_on_column) or self.largest_y_on_column(y, self.largest_y_on_column):
            return True
        return False

    def is_outside_map_border(self, pos):
        if self.outside_x(pos) or self.outside_y(pos):
            return True
        return False

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


        
    