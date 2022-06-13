
from tracemalloc import start
import pygame
import snake_rules
import better_rect
import Colors

class Game_Object:
    def __init__(self, GM, size = snake_rules.pixel_size, color = Colors.GREEN, start_pos = (0,0), corner_radius = 3, outline_width = 4, outline_color = Colors.BLACK, tag = "None"):
            self.GM = GM
           # self.position = start_pos
            self.tag = tag
            self.rect = better_rect.OutlinedSurface(start_pos,size,color,outline_color,outline_width,corner_radius)
 
    def update_events(self, event):
        pass

    def update_logic(self, delta_time):
        pass

    def on_collision(self, an_object):
        pass

    def fixed_update(self):
        pass

    def move(self, direction):
        move_amount = snake_rules.multiply_vectors(direction, snake_rules.step)
        self.rect.move(move_amount)
        self.GM.add_state_to_map_state(self.rect.get_position(), self.tag)

    def draw(self, screen):
        self.rect.draw(screen)

