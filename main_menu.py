
import pygame
import snake_rules
import Colors


class Button:
    def __init__(self, screen, size, position, text, color, s_color, t_color = Colors.BLACK, selected = False, on_press = None):
        self.screen = screen
        self.surf = pygame.Surface(size)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.rect = self.surf.get_rect()
        self.text = self.font.render(text,True,t_color)
        self.rect.center = [position[0], position[1]]
        self.t_rect = self.text.get_rect()
        self.t_rect.center = (position[0], position[1])
        self.color = color
        self.s_color = s_color
        self.selected = selected
        self.on_press = on_press

        if selected:
            self.on_selection()
        else:
            self.surf.fill(self.color)

    def on_selection(self):
        self.surf.fill(self.s_color)

    def on_press(self):
        self.on_press

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        screen.blit(self.text, self.t_rect)



class ButtonSet:
    def __init__(self, frame, margin_x, margin_y, default_dom_size, rows, columns, amount, texts, colors, s_colors, selection_index, on_press_args = None, top_down = True):
        self.screen = screen
        self.frame_x = (frame[0][0], frame[0][1])
        self.frame_y = (frame[1][0], frame[1][1])
        self.buttons = []

        self.frame_size = (self.frame_x[1] - self.frame_x[0], self.frame_y[1] - self.frame_y[0])
        self.estimated_button_size_sub = (self.frame_size[0] / columns) - 2 * margin_x
        self.estimated_button_size_dom = default_dom_size
        
        button_height = (rows / columns) * self.frame_size[1] - 2 * margin_y
        button_width = (columns / rows) * self.frame_size[0] - 2 * margin_x
        button_size = (button_width, button_height)
        print(button_size)
        pos_y = self.frame_y[0] + margin_y
        pos_x = self.frame_x[0] + margin_x

        current_row = 0
        current_column = 0

        for i in range(amount):

            pos_y = self.frame_y[0] + ((button_size[1] + (margin_y)) * current_row) + self.frame_y[0]
            pos_x = self.frame_x[0] + ((button_size[1] + (margin_x)) * current_column) + self.frame_x[0]

            self.buttons.append(Button(self.screen, button_size,(pos_x, pos_y), texts[i],colors[i], s_colors[i], on_press=on_press_args[i]))

            if current_row >= rows - 1:
                current_row = 0
                current_column += 1
            else:
                current_row += 1

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)



class MainMenu:
    def __init__(self):
        self.elements = [ButtonSet(((100,200),(100,200)), 5, 5, 0, 2,2,4,["1","1","1","1"],[Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN],[Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN],1,[None,None,None,None])]

    def draw(self, screen):
        for element in self.elements:
            element.draw(screen)

            

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(snake_rules.screen_size)
    pygame.display.set_caption("Menu")
    main_menu = MainMenu()
    update = True
    clock = pygame.time.Clock()

        
    while update:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update = False


    
        screen.fill(Colors.WHITE)
        main_menu.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
