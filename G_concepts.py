from random import random
import Colors
import snake_rules
import GameObject
import MapReader
import ConceptsAndClasses
import food
import UI

class GameConcepts():
    def __init__(self, map_string = "Map1.txt"):
        self.map_reader = MapReader.MapReader(map_string)
        
        self.preffered_food_amount = 1
        self.f_step_timer = 0
        self.update = True

        self.game_objects = []
        self.object_positions = []
        self.food = []

        UI_height = snake_rules.snake_UI_height
        self.true_res = snake_rules.add_vectors(self.map_reader.res, (0, UI_height))
        self.UI = UI.UserInterface(self.true_res)
        self.movement_events = ConceptsAndClasses.movement_event_handler()

        for position in self.map_reader.get_wall_positions():
            self.add_object_to_game(GameObject.Game_Object(self ,color=Colors.BLACK, start_pos=position, tag ="w"))
        
    def add_object_to_game(self, new_object):
        self.game_objects.append(new_object)

    def add_interface(self, snake):
        self.UI.add_snake_UI((10,self.true_res[1] - snake_rules.snake_UI_height- 10), (self.true_res[0]/ 3.5,snake_rules.snake_UI_height),snake=snake)

    def kill_object(self, an_object):
        if isinstance(an_object,GameObject.Game_Object) and an_object in self.game_objects:
            self.game_objects.remove(an_object)
            if isinstance(an_object, food.Food):
                self.food.remove(an_object)
        else:
            return "Object is, or cannot, be removed"

    def food_check(self):
        if len(self.food) < self.preffered_food_amount:
            self.add_food()
    
    def add_score_to_UI(self, new_score, snake):
        self.UI.set_score(new_score, snake)

    def add_food(self):
        random_pos = self.get_random_spawn()
        n_food = food.Food(self,start_pos=random_pos)

        self.game_objects.append(n_food)
        self.food.append(n_food)

    def add_movement_event(self, an_object, a_move):
        if an_object in self.game_objects:
            self.movement_events.add_event(an_object, a_move)
        else:
            return "Error! object cannot be moved"
    
    def draw(self, screen):
        for g_o in self.game_objects:
            g_o.draw(screen)
        
        self.UI.draw(screen)
    
    def get_random_spawn(self):
        object_rep = []
        for o in self.game_objects:
            new_pos = o.rect.get_position()
            object_rep.append((int(new_pos[0]), int(new_pos[1])))
            
        random_pos = self.map_reader.get_random_spawn_location()
        while random_pos in object_rep:
            random_pos = self.map_reader.get_random_spawn_location()

        return random_pos

    def collided_with_illegal(self):
        self.update = False

    
    def update_logic(self, delta_time):
        for g_o in self.game_objects:
            g_o.update_logic(delta_time)

        self.food_check()

        self.f_step_timer += 1
        if(self.movement_check()):
            self.f_step_timer = 0
        
        self.UI.update(delta_time)

    def update_events(self, event):
        for g_o in self.game_objects:
            g_o.update_events(event)

        self.UI.update_events(event)

    def movement_check(self):
        if self.f_step_timer >= snake_rules.f_step_interval:
            self.collision_check(self.movement_events.execute_events())
            return True
        return False

    def collision_check(self, moved_objects):
        if moved_objects != None:
            for m_o in moved_objects:
                for o in self.game_objects:
                    if m_o != o:
                        if m_o.rect.collides_with(o.rect):
                            m_o.on_collision(o)
                            o.on_collision(m_o)

