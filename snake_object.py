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

    def revert_previous_move(self):
        self.rect.set_position(self.old_pos)

    def move(self, direction):
        self.last_move = direction
        self.old_pos = self.rect.get_position()
        move_amount = snake_rules.multiply_vectors(direction, snake_rules.step)
        self.rect.move(move_amount)

        for i in range(1, len(self.body)):
            self.body[i].move(None)

    def add_length(self, amount):
        for i in range(amount):
            self.body.append(SnakeBodyObject(self.GM,follow_object=self.body[-1],snek=self, start_pos=self.body[-1].rect.get_position()))
        self.GM.add_score_to_UI(len(self.body), self)



class SnakeState():
    def __init__(self, position, room_map):
        self.position = position
        self.room_map = room_map
        self.actions = []
        
    def set_values(self, position, room_map):
        self.position = position
        self.room_map = room_map

    def create_node(self, position, room_map, action):
        new_node = copy.deepcopy(self)
        new_node.set_values(position, room_map)
        new_node.actions.append(action)
        return new_node
    
    def move_dir(self, direction):
        new_pos = snake_rules.add_vectors(self.position, direction)
        new_map = self.room_map.copy()

        map_item = new_map.get(new_pos)

        if map_item == None:
            return self.create_node(new_pos, new_map, snake_rules.dir_to_string(direction))
        if map_item == "w":
            return None
        elif map_item == "f":
            new_map.pop(new_pos)
            return self.create_node(new_pos, new_map, snake_rules.dir_to_string(direction))
    
    def expand(self):
        nodes = []
        
        nodes.append(self.move_dir(snake_rules.multiply_vector(snake_rules.right, 24)))
        nodes.append(self.move_dir(snake_rules.multiply_vector(snake_rules.left, 24)))
        nodes.append(self.move_dir(snake_rules.multiply_vector(snake_rules.up, 24)))
        nodes.append(self.move_dir(snake_rules.multiply_vector(snake_rules.down, 24)))
            
        return list(filter(None, nodes))
    
    def get_position(self):
        """Get the position of the agent"""
        return self.position

    def get_food(self):
        """Get the position of all food as a list"""
        food_map = []
        for key, value in self.room_map.items():
            if value == "f":
                food_map.append(key)

        return food_map
        
    def reached_goal(self):
        if self.get_food() == []:
            return True
        return False

    def get_actions(self):
        """Return all the actions neccessary to reach this state"""
        return self.actions
        
            


class AI_Test(Snake):
    def __init__(self, GM, size=snake_rules.pixel_size, color=Colors.BLACK, start_pos=(0, 0), tag="sh", length=2):
        super().__init__(GM, size, color, start_pos, tag, length)
        self.next_moves = []
        self.move_count = 0


    def get_map_representation(self):
        return self.GM.map_state

    def fixed_update(self):
        if self.next_moves == []:
            self.next_moves = self.search()
        else:
            self.move_count += 1

        print (self.next_moves)
    
        self.GM.add_movement_event(self, snake_rules.string_to_dir(self.next_moves[self.move_count]))
      

    def search(self):
        start_node = SnakeState(self.rect.get_position(), self.get_map_representation())
        return(self.A_star(start_node))

    def on_collision(self, an_object):
        if an_object.tag == "f":
            print("UWT")
            self.reset_search()
        
        return super().on_collision(an_object)

    def reset_search(self):
        self.move_count = 0
        self.next_moves = []


    def is_duplicate(self, expanded, node):
        for n in expanded:
            if n.get_position() == node.get_position() and n.room_map == node.room_map:
                    return True
        return False
        
    def A_star(self, start_state):
        #best-first search that uses the evaluation function f(n) = g(n) + h(n)
        #g(n) = estimated path cost from initial state to node n
        #h(n) = estimated cost from the shorthest path from n to goal state
        #f(n) = estimated cost of the best path that continiues from n to goal
        
        explored = []
        frontier = [start_state]
        
        def closest_food(position, food_list):
            closest_distance = 10000
            closest_node = (0,0)
            
            for f_pos in food_list:
                moves_x = abs(f_pos[0] - position[0])
                moves_y = abs(f_pos[1] - position[1])
                moves_total = moves_x + moves_y
                if moves_total < closest_distance:
                    closest_node = f_pos
            
            return closest_node
        
        #heuristik funktion
        def heuristic(state):
            #Estimering av handlingskostnaden till vald nod
            curr_action_cost = len(state.get_actions())
            #Estimering av kortaste handlingkostnad till mål
            rough_estimate_cost_goal = 0
            
            
            curr_pos = state.get_position()
            food_list = state.get_food()
            food_copy = food_list.copy()
            food_sorted = []
            #räkna ut alla möjliga vägar -> välj den kortaste
            
            for node in food_copy:
                closest = closest_food(curr_pos, food_copy)
                if closest in food_copy:
                    food_copy.remove(closest)
                    
                food_sorted.append(closest)
                curr_pos = closest
                
            #print(food_list)
            #print(food_sorted)
                
            for f_pos in food_sorted:
                moves_x = abs(f_pos[0] - curr_pos[0])
                moves_y = abs(f_pos[1] - curr_pos[1])
                moves_total = moves_x + moves_y
                rough_estimate_cost_goal += moves_total
            
            #Vag estimering av kortaste vägkostnad från start_nod till mål
            return (curr_action_cost + rough_estimate_cost_goal)
        
        #Sökande
        while len(frontier) > 0:
            if len(explored) >= 10000:
                break
                
            frontier.sort(key=lambda n: heuristic(n))
            node = frontier.pop(0)
            
            #Två noder är likadana om de var i samma position och går i samma riktning
            if self.is_duplicate(explored, node):
                continue
            
            if node.reached_goal():
                return node.get_actions()
                
            frontier.extend(node.expand())
            explored.append(node)
        

    
        


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

