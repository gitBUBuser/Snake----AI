import pygame
import snake_rules
import Colors

class GameObject(pygame.sprite.Sprite):
    def __init__(self):
            super(GameObject, self).__init__()
            self.surf = pygame.surface(snake_rules.pixel_size[0], snake_rules.pixel_size[1])
            self.surf.fill(Colors.GREEN)
            self.rect = self.surf.get_rect()
            
 
    def update(event):
        pass

