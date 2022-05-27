import pygame
import Colors
import snake_rules
import GameObject
import snake_object
import MapReader
import ConceptsAndClasses
import food
import python_utils

pygame.init()

class GameConcepts():
    def __init__(self):
        self.map_reader = MapReader.MapReader("Map1.txt")
        self.game_objects = []
        self.object_positions = []
        self.map_state = {}
        self.food = []



        for position in self.map_reader.get_wall_positions():
            self.add_object_to_game(GameObject.Game_Object(self ,color=Colors.BLACK, start_pos=position, tag ="w"))
            self.map_state[position] = "w"

        

        for key, value in self.map_state.items():
            print(str(key) + " | " +  str(value))
        self.movement_events = ConceptsAndClasses.movement_event_handler()
        
    def add_object_to_game(self, new_object):
        self.game_objects.append(new_object)

    def kill_object(self, an_object):
        if isinstance(an_object,GameObject.Game_Object) and an_object in self.game_objects:
            self.game_objects.remove(an_object)
            if isinstance(an_object, food.Food):
                self.food.remove(an_object)
        else:
            return "Object is, or cannot, be removed"

    def food_check(self):
        if len(self.food) < 1:
            self.add_food()
        
    def add_food(self):
        object_rep = []
        for o in self.game_objects:
            shei = o.rect.get_position()
            object_rep.append((int(shei[0]), int(shei[1])))
            
        rando_pos = self.map_reader.get_random_spawn_location()

        while rando_pos in object_rep:
            print("respawn")
            rando_pos = self.map_reader.get_random_spawn_location()
        
        n_food = food.Food(self,start_pos=rando_pos, tag="f")
        self.map_state[rando_pos] = "f"
        self.game_objects.append(n_food)
        self.food.append(n_food)
        """n_food = food.Food(self, start_pos=(144,144), tag = "f")
        self.map_state[(144,144)] = "f"
        self.game_objects.append(n_food)"""
    
    def clear_moving_map(self):
        poppers = []
        for key, value in self.map_state.items():
            if value != "w" or value != "f":
                poppers.append(key)
        for pops in poppers:
            self.map_state.pop(pops)

    def is_there_food(self, wanted_food_count):
        return len(self.food) < wanted_food_count

    def add_movement_event(self, an_object, a_move):
        if an_object in self.game_objects:
            self.movement_events.add_event(an_object, a_move)
        else:
            return "Error! object cannot be moved"
        
g_concepts = GameConcepts()

screen = pygame.display.set_mode(g_concepts.map_reader.res)
pygame.display.set_caption("SneakySnake")
f_timer_movement = 0

g_concepts.add_object_to_game(snake_object.AI_Test(g_concepts, start_pos = (72,72), tag="sh"))


clock = pygame.time.Clock()
update = True

def update_events(event):
    for g_o in g_concepts.game_objects:
        g_o.update_events(event)

def collision_check(moved_objects):
    if moved_objects != None:
        for m_o in moved_objects:
            for o in g_concepts.game_objects:
                if m_o != o:
                    if m_o.rect.collides_with(o.rect):
                        m_o.on_collision(o)
                        o.on_collision(m_o)
    
def movement_check():
    if f_timer_movement >= snake_rules.f_step_interval:
        for g_o in g_concepts.game_objects:
            g_o.fixed_update()
        g_concepts.clear_moving_map()
        collision_check(g_concepts.movement_events.execute_events())
        return True
    return False
    
def update_logic():
    g_concepts.food_check()
    for g_o in g_concepts.game_objects:
        g_o.update_logic()
        
def draw():
    for g_o in g_concepts.game_objects:
        g_o.draw(screen)

while update:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update = False
        update_events(event)

    update_logic()
    f_timer_movement += 1
    if(movement_check()):
        f_timer_movement = 0
    
    screen.fill(Colors.BACKGROUND_GRAY)
    draw()
    pygame.display.flip()

    clock.tick(snake_rules.f_rate)
pygame.quit()