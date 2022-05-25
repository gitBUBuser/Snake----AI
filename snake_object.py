from tracemalloc import start
import pygame
import GameObject
import snake_rules
import Colors

    
class Snake(GameObject.Game_Object):
    def __init__(self, GM, size=snake_rules.pixel_size, color=Colors.GREEN, start_pos=(0, 0), tag="None", length = 2):
        super().__init__(size,GM, color, start_pos, tag)
        self.move_dir = (0,0)
        self.body = []
        self.last_move = ()
        self.length = length
        self.body.append(self)
 
        for i in range(1, self.length):
            self.body.append(SnakeBodyObject(self.GM,follow_object=self.body[i-1],snek=self, start_pos=self.position))


    def control(self):
        pass

    def on_collision(self, an_object):
        if an_object.tag == "Wall":
            self.revert_previous_move()
        elif an_object.tag == "Food":
            self.add_length(2)
        return super().on_collision(an_object)

    def update_events(self, event):
        return super().update_events(event)

    def revert_previous_move(self):
        self.position = self.old_pos
        self.rect.update(self.old_pos, self.rect.size)

    def move(self, direction):
        self.last_move = direction
        self.old_pos = self.position
        move_amount = snake_rules.multiply_vectors(direction, snake_rules.step)
        self.rect.move_ip(move_amount)
        self.position = snake_rules.add_vectors(self.position, move_amount)

        for i in range(1, len(self.body)):
            self.body[i].move(None)

        
    def add_length(self, amount):
        for i in range(amount):
            self.body.append(SnakeBodyObject(self.GM,follow_object=self.body[-1],snek=self, start_pos=self.body[-1].position))
            
    def step(self, direction):
        pass
        #self.old_positions.append(self.position)
        #self.last_move = direction
        #for i in range(len(self.body)):
        #    self.body[i].step(self.old_positions[-i - 1])
        #return super().step(direction)

    def update_logic(self):
        return super().update_logic()

class PlayerSnake(Snake):
    def __init__(self,GM, size=snake_rules.pixel_size, color=Colors.GREEN, start_pos=(0, 0), tag="None", length = 2):
        super().__init__(size,GM, color, start_pos, tag, length)

    def control(self):
        return super().control()


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

    def update_logic(self):
        self.GM.add_movement_event(self, self.move_dir)
    

class SnakeBodyObject(GameObject.Game_Object):
     def __init__(self, GM, follow_object, snek, size = snake_rules.pixel_size, color = Colors.RED, start_pos = (0,0), tag = "None"):
        super().__init__(GM, size, color, start_pos, tag)
        self.snek = snek
        self.parent = follow_object

        self.GM.add_object_to_game(self)


     def move(self, direction):
         self.old_pos = self.position
         self.rect.update(self.parent.old_pos[0], self.parent.old_pos[1], snake_rules.pixel_size[0], snake_rules.pixel_size[1])
         self.position = self.parent.old_pos

