
import pygame
import snake_rules
import Colors

class BestSurface():
    def __init__(self, position, size, color, corner_radius=0):
        self.size = size
        self.color = color
        self.corner_radius = corner_radius
        self.position = position

        self.surface = pygame.Surface(self.size)
        self.rect = self.surface.get_rect()

        self.set_position(position)

    def set_position(self, new_position):
        self.position = new_position
        self.rect.update(self.position, self.size)

    def move(self, movement_vector):
        self.position = snake_rules.add_vectors(self.position, movement_vector)
        self.rect.move_ip(movement_vector)

    def set_size(self, new_size):
        self.size = new_size
        self.surface = pygame.transform.scale(self.surface, self.size)
    
    def set_color(self, new_color):
        self.color = new_color

    def update_rect(self):
        self.rect.update(self.position, self.size)
    
    def get_position(self):
        return self.position

    def get_size(self):
        return self.size

    def get_outer_rect(self):
        return self.rect
    
    def collides_with(self, a_rect):
        return self.get_outer_rect().colliderect(a_rect.get_outer_rect())
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.corner_radius)


class OutlinedSurface(BestSurface):
    def __init__(self, position, size, color = Colors.GREEN, outline_color = Colors.BLACK, outline_width = 0, corner_radius=0):

        self.t_size = size
        self.t_position = position
        self.o_color = outline_color
        self.o_width = outline_width
        
        self.o_surface = pygame.Surface(self.t_size)
        self.o_rect = self.o_surface.get_rect()

        super().__init__(self.t_position, self.t_to_inner_size(self.t_size), color, corner_radius)


        self.set_size(self.t_size)
        self.update_rect()
        

    def t_to_inner_position(self, a_position):
        return (int(a_position[0] + (self.o_width * 0.5)), int(a_position[1] + (self.o_width * 0.5)))

    def t_to_inner_size(self, a_size):
        return (a_size[0] - self.o_width, a_size[1] - self.o_width)
    
    def update_rect(self):
        self.o_rect.update(self.t_position, self.t_size)
        return super().update_rect()


#OBS!!!! KANSKE FÅR ÄNDRA SÅ MOVEMENT BLIR RELATIVT TILL NY GREJ
    def move(self, movement_vector):
        self.t_position = snake_rules.add_vectors(self.t_position, movement_vector)
        self.o_rect.move_ip(movement_vector)
        return super().move(movement_vector)

    def set_position(self, new_position):
        self.t_position = new_position
        self.o_rect.update(self.t_position, self.t_size)
        self.position = self.t_to_inner_position(self.t_position)
        self.rect.update(self.position, self.size)
    
    def set_size(self, new_size):
        self.t_size = new_size
        self.o_surface = pygame.transform.scale(self.o_surface, new_size)
        super().set_size(self.t_to_inner_size(self.t_size))
        self.update_rect()

    def set_outline_color(self, new_color):
        self.o_color = new_color
    
    def draw(self, screen):

        pygame.draw.rect(screen, self.o_color, self.o_rect, border_radius=self.corner_radius)
        return super().draw(screen)

    def get_position(self):
        return self.t_position

    def get_size(self):
        return self.t_size

    def get_outer_rect(self):
        return self.o_rect


"""if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(snake_rules.screen_size)
    pygame.display.set_caption("Menu")

    #other_test = BestSurface((200,200), (100,100), Colors.LIGHT_BLUE)
    third_test = OutlinedSurface((100,10),(100,100),corner_radius=10, outline_width=50)
    update = True
    clock = pygame.time.Clock()

        
    while update:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update = False
            if event.type == pygame.KEYDOWN:
                if event.key == snake_rules.down_key:
                    third_test.move(snake_rules.multiply_vector(snake_rules.down, 10))

                if event.key == snake_rules.up_key:
                    third_test.move(snake_rules.multiply_vector(snake_rules.up, 10))

                if event.key == snake_rules.right_key:
                    third_test.move(snake_rules.multiply_vector(snake_rules.right, 10))

                if event.key == snake_rules.left_key:
                    third_test.move(snake_rules.multiply_vector(snake_rules.left, 10))

        screen.fill(Colors.WHITE)
        third_test.draw(screen)
        #other_test.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()"""