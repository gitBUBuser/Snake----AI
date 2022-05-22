import pygame
import Colors
import snake_rules
import GameObject
import snake_object
import MapReader
import ConceptsAndClasses

pygame.init()



size = (snake_rules.screen_size)

map_reader = MapReader.MapReader("Map1.txt")

screen = pygame.display.set_mode(map_reader.res)
f_timer_movement = 0
pygame.display.set_caption("SneakySnake")

class GameConcepts():
    def __init__(self):
        self.game_objects = []
        print("INIT!")
        self.movement_events = movement_events = ConceptsAndClasses.movement_event_handler()
        
    def add_object_to_game(self, new_object):
        self.game_objects.append(new_object)


    def kill_object(self, an_object):
        if type(an_object) == GameObject.Game_Object and an_object in self.game_objects:
            self.game_objects.remove(an_object)
        else:
            return "Object is, or cannot, be removed"

    def add_movement_event(self, an_object, a_move):
        if an_object in self.game_objects:
            self.movement_events.add_event(an_object, a_move)
        else:
            return "Error! object cannot be moved"
        
g_concepts = GameConcepts()
g_concepts.add_object_to_game(snake_object.PlayerSnake(g_concepts, start_pos = (24,24)))

for position in map_reader.get_wall_positions():
    g_concepts.add_object_to_game(GameObject.Game_Object(g_concepts,color=Colors.BLACK, start_pos=position))
clock = pygame.time.Clock()
update = True

def update_events(event):
    for g_o in g_concepts.game_objects:
        g_o.update_events(event)


def movement_check():
    if f_timer_movement >= snake_rules.f_step_interval:
        g_concepts.movement_events.execute_events()
        return True
    return False
    
def update_logic():
    for g_o in g_concepts.game_objects:
        g_o.update_logic()
        
def draw():
    for g_o in g_concepts.game_objects:
        screen.blit(g_o.surf, g_o.rect)

while update:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update = False
        update_events(event)

    update_logic()
    f_timer_movement += 1
    if(movement_check()):
        f_timer_movement = 0
    
    screen.fill(Colors.WHITE)
    draw()
    pygame.display.flip()

    clock.tick(60)
pygame.quit()
