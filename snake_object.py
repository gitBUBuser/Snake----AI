from re import search
import pygame
import GameObject
import snake_rules
import Colors
import copy
import better_rect
import python_utils

    
class Snake(GameObject.Game_Object):
    def __init__(self, GM, size=snake_rules.pixel_size, color=Colors.AMNIENT_GREEN, start_pos=(0, 0), tag="sh", length = 2):
        super().__init__(GM, size, color,start_pos,tag=tag, corner_radius=10)
        
        self.move_dir = (0,0)
        self.body = []
        self.last_move = ()
        self.old_pos = start_pos
        self.length = length
        
        # Adds user interface for the snake
        self.GM.add_interface(self)

        self.body.append(self)
        for i in range(1, self.length):
            self.body.append(SnakeBodyObject(self.GM,follow_object=self.body[i-1],snek=self, start_pos=start_pos))


    def control(self):
        pass

    def on_collision(self, an_object):
        if an_object.tag == "w":
            self.GM.collided_with_illegal()
        if an_object.tag == "s" and len(self.body) > 3:
            self.GM.collided_with_illegal()
        return super().on_collision(an_object)

    def update_events(self, event):
        return super().update_events(event)

    def update_logic(self, delta_time):
        return super().update_logic(delta_time)

    def revert_previous_move(self):
        self.rect.set_position(self.old_pos)

    def move(self, direction):
        self.last_move = direction
        self.old_pos = self.rect.get_position()
        super().move(direction)

        for i in range(1, len(self.body)):
            self.body[i].move(None)

    def add_length(self, amount):
        for i in range(amount):
            self.body.append(SnakeBodyObject(self.GM,follow_object=self.body[-1],snek=self, start_pos=self.body[-1].rect.get_position()))
        self.GM.add_score_to_UI(len(self.body), self)

class PlayerSnake(Snake):
    def __init__(self,GM, size=snake_rules.pixel_size, color=Colors.AMNIENT_GREEN, start_pos=(0, 0), tag="sh", length = 2):
        super().__init__(GM, size, color, start_pos, tag, length)

    def update_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == snake_rules.down_key and self.last_move != snake_rules.up:
                self.move_dir = snake_rules.down

            if event.key == snake_rules.up_key and self.last_move != snake_rules.down:
                self.move_dir = snake_rules.up

            if event.key == snake_rules.right_key and self.last_move != snake_rules.left:
                self.move_dir = snake_rules.right

            if event.key == snake_rules.left_key and self.last_move != snake_rules.right:
                self.move_dir = snake_rules.left

        return super().update_events(event)

    def update_logic(self, delta_time):
        self.GM.add_movement_event(self, self.move_dir)
    

class SnakeBodyObject(GameObject.Game_Object):
     def __init__(self, GM, follow_object, snek, size = snake_rules.pixel_size, color = Colors.SOFT_RED, start_pos = (0,0), tag = "s"):
        super().__init__(GM, size, color, start_pos, tag=tag)
        self.snek = snek
        self.old_pos = start_pos
        self.parent = follow_object

        self.GM.add_object_to_game(self)


     def move(self, direction):
         self.old_pos = self.rect.get_position()
         self.rect.set_position((self.parent.old_pos[0], self.parent.old_pos[1]))
         self.GM.add_state_to_map_state(self.rect.get_position(), self.tag)

