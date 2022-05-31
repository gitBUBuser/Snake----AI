import G_concepts
import pygame
import Colors
import snake_rules
import snake_object

pygame.init()

quit = False

while not quit:
    ticks_last_frame = 0
    g_concepts = G_concepts.GameConcepts()
    screen = pygame.display.set_mode(g_concepts.true_res)

    pygame.display.set_caption("SneakySnake")
    g_concepts.add_object_to_game(snake_object.PlayerSnake(g_concepts, start_pos = g_concepts.get_random_spawn(), tag="sh"))

    clock = pygame.time.Clock()

    while g_concepts.update:
        t = pygame.time.get_ticks()
        delta_time = (t - ticks_last_frame) / 1000.0
        ticks_last_frame = t

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g_concepts.update = False
                quit = True    
            g_concepts.update_events(event)

        g_concepts.update_logic(delta_time)

        screen.fill(Colors.BACKGROUND_GRAY)
        g_concepts.draw(screen)
        pygame.display.flip()

        clock.tick(snake_rules.f_rate)

    
pygame.quit()


