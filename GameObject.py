import pygame
import snake_rules
import Colors

class Game_Object:
    def __init__(self, GM, size = snake_rules.pixel_size, color = Colors.GREEN, start_pos = (0,0)):
            self.GM = GM
            self.surf = pygame.Surface(size)
            self.surf.fill(color)
            self.rect = self.surf.get_rect()
            self.position = start_pos
            self.move(start_pos)
            
 
    def update_events(self, event):
        pass

    def update_logic(self):
        pass

    def move(self, direction):
        self.rect.move_ip(direction)
    
    def step(self, direction):
        move_amount = snake_rules.multiply_vectors(direction, snake_rules.step)
        self.rect.move_ip(move_amount)
        self.position = snake_rules.add_vectors(self.position, move_amount)

