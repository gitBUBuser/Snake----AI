import pygame
import GameObject
import snake_rules
import Colors

class Food(GameObject.Game_Object):
    def __init__(self, GM, size=snake_rules.pixel_size, color=Colors.RED, start_pos=(0, 0), tag="Food"):
        super().__init__(GM, size, color, start_pos, tag)

    def on_collision(self, an_object):
        self.GM.kill_object(self)

