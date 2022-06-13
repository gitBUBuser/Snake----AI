

import snake_object as s_o
import snake_rules
import Colors
import random


"""
    Randomly tweak the knobs and cables driving our neural network to create an initial set of unique versions.
    Let each of those neural nets play Snake.
    After every neural net has finished a game, select which neural nets performed best.
    Create a new generation of unique neural networks based on randomly tweaking those top performing neural nets.
    Repeat from step 2.
"""

# behöver veta - vilken riktning är maten
# vart kan jag röra mig utan att dö

class AI_snake(s_o.Snake):
    def __init__(self, GM, size=snake_rules.pixel_size, color=Colors.AMNIENT_GREEN, start_pos=(0, 0), tag="sh", length=2):
        super().__init__(GM, size, color, start_pos, tag, length)
        self.fitness = 0
        self.move_count = 0
    
    def get_map_representation(self):
        return self.GM.map_state
    
    def get_food_position(self):
        positions = []
        for foods in self.GM.food:
            positions.append(foods.rect.get_position())
        return positions
        
    def fixed_update(self):
        self.GM.add_movement_event(self, self.move_dir)
        return super().fixed_update()

    def simulate_move(self, move):
        map = self.get_map_representation()
        new_pos = snake_rules.add_vectors(self.rect.get_position(), move)

        map_item = map.get(new_pos)
        if map_item == None:
            return "clear"
        if map_item == "f":
            return "food"
        if map_item == "w" or "s" or "sh":
            return "death"

        return "error"

     # Returns the left move direction from the Snake's POV
    def left_dir(self):
        return (self.move_dir[1], - self.move_dir[0])

    # Returns the right move direction from the Snake's POV
    def right_dir(self):
        return (-self.move_dir[1], self.move_dir[0])

    # Returns the forward step from the Snake's POV
    def step_ahead(self):
        return snake_rules.multiply_vectors(self.move_dir, snake_rules.step)

    # Returns the left step from the Snake's POV
    def step_left(self):
        return snake_rules.multiply_vectors(self.left_dir(), snake_rules.step)

    # Returns the right step from the Snake's POV
    def step_right(self):
        return snake_rules.multiply_vectors(self.right_dir(), snake_rules.step)







class Modified_AI_Snake(AI_snake):
    def __init__(self, GM, size=snake_rules.pixel_size, color=Colors.AMNIENT_GREEN, start_pos=(0, 0), tag="sh", length=2):
        super().__init__(GM, size, color, start_pos, tag, length)
        

    def clear_ahead(self):
        result = self.simulate_move(self.step_ahead())
        if result == "clear" or result == "food":
            return True
        return False

    def clear_to_the_left(self):
        result = self.simulate_move(self.step_left())
        if result == "clear" or result == "food":
            return True
        return False
    
    def clear_to_the_right(self):
        result = self.simulate_move(self.step_right())
        if result == "clear" or result == "food":
            return True
        return False

    def food_in_direction(self, dir):
        x = dir[0]
        y = dir[1]

        for food_p in self.get_food_position():
            dir_to_food = snake_rules.subtract_vectors(self.rect.get_position(), food_p)
            if y == 0:
                if (x > 0 and dir_to_food[0] < 0) or (x < 0 and dir_to_food[0] > 0):
                    return True
            else:
                if (y > 0 and dir_to_food[1] < 0) or (y < 0 and dir_to_food[1] > 0):
                    return True

        return False

    def food_ahead(self): 
        return self.food_in_direction(self.move_dir)
    

    def food_left(self): 
        return self.food_in_direction(self.left_dir())


    def food_right(self): 
        return self.food_in_direction(self.right_dir())


class test_snake(Modified_AI_Snake):
    def __init__(self, GM, size=snake_rules.pixel_size, color=Colors.AMNIENT_GREEN, start_pos=(0, 0), tag="sh", length=2):
        super().__init__(GM, size, color, start_pos, tag, length)
        self.move_dir = snake_rules.up

    def fixed_update(self):

        clear_ahead = self.clear_ahead()
        clear_to_the_left = self.clear_to_the_left()
        clear_to_the_right = self.clear_to_the_right()

        food_ahead = self.food_ahead()
        food_to_the_left = self.food_left()
        food_to_the_right = self.food_right()

        if clear_ahead:
            if food_ahead:
                return super().fixed_update()

        if food_to_the_left:
            if clear_to_the_left:
                self.move_dir = self.left_dir()
                return super().fixed_update()
            else:
                if clear_ahead:
                    return super().fixed_update()
                elif clear_to_the_right:
                    self.move_dir = self.right_dir()
                    return super().fixed_update()
        
        if food_to_the_right:
            if clear_to_the_right:
                self.move_dir = self.right_dir()
                return super().fixed_update()
            else:
                if clear_ahead: 
                    return super().fixed_update()
                elif clear_to_the_left:
                    self.move_dir = self.left_dir()
                    return super().fixed_update()
        
        if not clear_ahead and not food_to_the_left and not food_to_the_right:
            rng = random.random()
            if rng > 0.5:
                print ("bigger")
                if clear_to_the_right:
                    self.move_dir = self.right_dir()
                else:
                    self.move_dir = self.left_dir()
            else:
                print("smaller")
                if clear_to_the_left:
                    self.move_dir = self.left_dir()
                else:
                    self.move_dir = self.right_dir()


        return super().fixed_update()
        




        

  
            
