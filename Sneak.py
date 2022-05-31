
from multiprocessing.spawn import get_command_line
import pygame
import Colors
import snake_rules
import UI_extras
import GameObject
import snake_object
import MapReader
import ConceptsAndClasses
import food
import UI
pygame.init()



        
g_concepts = GameConcepts()

screen = pygame.display.set_mode(g_concepts.true_res)
pygame.display.set_caption("SneakySnake")



f_timer_movement = 0
getTicksLastFrame = 0
g_concepts.add_object_to_game(snake_object.PlayerSnake(g_concepts, start_pos = (72,72), tag="sh"))


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

    g_concepts.UI.draw(screen)


while update:
    t = pygame.time.get_ticks()
    delta_time = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update = False
        update_events(event)
        g_concepts.UI.update_events(event)

    update_logic()
    f_timer_movement += 1
    if(movement_check()):
        f_timer_movement = 0
    g_concepts.UI.update(delta_time)


    screen.fill(Colors.BACKGROUND_GRAY)
    draw()
    pygame.display.flip()

    clock.tick(snake_rules.f_rate)
pygame.quit()
