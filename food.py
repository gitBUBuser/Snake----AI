import colorsys
import pygame
import GameObject
import snake_rules
import Colors

class Food(GameObject.Game_Object):
    def __init__(self, GM, size=snake_rules.pixel_size, color=Colors.DEEP_PURPLE, feed_amount = 2, start_pos=(0, 0), tag="f"):
        super().__init__(GM, size=size, color=color, start_pos=start_pos,corner_radius=10,outline_width=4,outline_color=Colors.BLACK,tag="f" )
        self.feed_amount = feed_amount
        print(self.rect.get_position())

    def on_collision(self, an_object):
        if an_object.tag == "sh":
            an_object.add_length(self.feed_amount)
            self.GM.kill_object(self)


