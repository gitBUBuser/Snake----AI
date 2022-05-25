
import pygame
import Colors
import snake_rules
import GameObject
import snake_object
import MapReader
import ConceptsAndClasses
import food
pygame.init()


class GameConcepts():
    def __init__(self):
        self.map_reader = MapReader.MapReader("Map1.txt")
        self.game_objects = []
        self.object_positions = []
        self.food = []

        for position in self.map_reader.get_wall_positions():
            self.add_object_to_game(GameObject.Game_Object(self ,color=Colors.BLACK, start_pos=position, tag ="Wall"))

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
        
        n_food = food.Food(self,start_pos=rando_pos)

        self.game_objects.append(n_food)
        self.food.append(n_food)
    

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

g_concepts.add_object_to_game(snake_object.PlayerSnake(g_concepts, start_pos = (240,240), tag="Snake"))


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
