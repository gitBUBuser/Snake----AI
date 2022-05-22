from tracemalloc import start
import pygame
import GameObject
import snake_rules
import Colors

    
class Snake(GameObject.Game_Object):
    def __init__(self, GM, size=snake_rules.pixel_size, color=Colors.GREEN, start_pos=(0, 0), start_length = 6):
        super().__init__(size,GM, color, start_pos)
        self.move_dir = (0,0)
        self.body = []
        self.old_moves = []
        self.old_positions = []
        for i in range(start_length):
            self.old_positions.append(start_pos)
            self.body.append(SnakeBodyObject(self.GM, start_pos=self.position))


    def control(self):
        pass

    def update_events(self, event):
        return super().update_events(event)

    def step(self, direction):
        self.old_positions.append(self.position)
        for i in range(len(self.body)):
            self.body[i].step(self.old_positions[-i - 1])
        return super().step(direction)

    def update_logic(self):
        return super().update_logic()

class PlayerSnake(Snake):
    def __init__(self,GM, size=snake_rules.pixel_size, color=Colors.GREEN, start_pos=(0, 0), start_length = 0):
        super().__init__(size,GM, color, start_pos)

    def control(self):
        move_vec = snake_rules.multiply_vectors(snake_rules.step, self.move_dir)
        self.rect.move_ip(move_vec)
        return super().control()


    def update_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == snake_rules.down_key:
                self.move_dir = snake_rules.down

            if event.key == snake_rules.up_key:
                self.move_dir = snake_rules.up

            if event.key == snake_rules.right_key:
                self.move_dir = snake_rules.right

            if event.key == snake_rules.left_key:
                self.move_dir = snake_rules.left

        return super().update_events(event)

    def update_logic(self):
        self.GM.add_movement_event(self, self.move_dir)
    

class SnakeBodyObject(GameObject.Game_Object):
     def __init__(self, GM, size = snake_rules.pixel_size, color = Colors.RED, start_pos = (0,0)):
        super().__init__(GM, size, color, start_pos)
        self.GM.add_object_to_game(self)

     def step(self, direction):
         self.rect.update(direction[0],direction[1], direction[0], direction[1])

