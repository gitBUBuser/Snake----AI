import pygame
import Colors
import snake_rules
import GameObject

pygame.init()

size = (snake_rules.screen_size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SneakySnake")

snake_pos_x = 0
snake_pos_y = 0
obje = GameObject.Game_Object(start_pos=(32,32))
game_objects = [obje]

clock = pygame.time.Clock()
update = True



def update_logic(event):
    for g_o in game_objects:
        g_o.update(event)

        
def draw():
    for g_o in game_objects:
        screen.blit(g_o.surf, g_o.rect)

while update:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            #update all game objects (with event)
            update = False

        update_logic(event)

        screen.fill(Colors.WHITE)
        draw()
        pygame.display.flip()
    clock.tick(60)


pygame.quit()
