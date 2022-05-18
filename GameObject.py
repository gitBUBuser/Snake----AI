import pygame
import snake_rules
import Colors

class Game_Object:

    def __init__(self, size = snake_rules.pixel_size, color = Colors.GREEN, start_pos = (0,0)):
            self.surf = pygame.Surface(size)
            self.surf.fill(color)
            self.rect = self.surf.get_rect()
            self.rect.move_ip(start_pos)
            
 
    def update(self, event):
        pass

