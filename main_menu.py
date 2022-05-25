
import pygame
import snake_rules
import Colors
import better_rect


class Button:
    def __init__(self,size, position, text, color, s_color, t_color = Colors.BLACK, selected = False, on_press = None):
        self.surf = pygame.Surface(size)
        self.size = size

        self.rect = better_rect.OutlinedSurface(position, size, color, corner_radius=10, outline_width=6)
        self.shrink_value = -6
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.pos = position
        self.text = self.font.render(text,True,t_color)
   
        self.t_rect = self.text.get_rect()
        self.t_rect.move_ip(position)
        self.color = color
        self.s_color = s_color
        self.selected = selected
        self.on_press = on_press

        if selected:
            self.on_selection()
        else:
            self.surf.fill(self.color)

    def on_selection(self):
        self.shrink()
        self.rect.set_color(self.s_color)
        

    def on_deselection(self):
        self.unshrink()
        self.rect.set_color(self.color)
        #self.rect.update(self.pos, self.size)
        

    def on_press(self):
        self.on_press
    
    def shrink(self):
        new_size = (self.size[0] - self.shrink_value, self.size[1] - self.shrink_value)
        new_pos = (self.pos[0] + (self.shrink_value / 2), self.pos[1] + (self.shrink_value / 2))
        self.rect.set_size(new_size)
        self.rect.set_position(new_pos)


    def unshrink(self):
        self.rect.set_size(self.size)
        self.rect.set_position(self.pos)

    def draw(self, screen):
        self.rect.draw(screen)





class ButtonSet:
    def __init__(self, frame, margin_x, margin_y, default_dom_size, rows, columns, amount, texts, colors, s_colors, selection_index, on_press_args = None, top_down = True):
        self.frame_x = (frame[0][0], frame[0][1])
        self.frame_y = (frame[1][0], frame[1][1])
        self.button_index = selection_index
        self.buttons = []

        self.frame_size = (self.frame_x[1] - self.frame_x[0], self.frame_y[1] - self.frame_y[0])
        self.estimated_button_size_sub = (self.frame_size[0] / columns) - 2 * margin_x
        self.estimated_button_size_dom = default_dom_size
        
        button_height = (self.frame_size[1] / rows) - 2 * margin_y
        button_width = (self.frame_size[0] / columns) - 2 * margin_x
        button_size = (button_width, button_height)
        print(button_size)
        pos_y = self.frame_y[0] + margin_y
        pos_x = self.frame_x[0] + margin_x

        current_row = 0
        current_column = 0

        for i in range(amount):

            pos_y = self.frame_y[0] + ((button_size[1] + (margin_y)) * current_row)
            pos_x = self.frame_x[0] + ((button_size[0] + (margin_x)) * current_column)
            if i == selection_index:
                self.buttons.append(Button(button_size,(pos_x, pos_y), texts[i],colors[i], s_colors[i], on_press=on_press_args[i], selected=True))
            else:
                self.buttons.append(Button(button_size,(pos_x, pos_y), texts[i],colors[i], s_colors[i], on_press=on_press_args[i]))

            if current_row >= rows - 1:
                current_row = 0
                current_column += 1
            else:
                current_row += 1

    def next_button(self):
        if self.button_index < len(self.buttons) - 1:
            self.buttons[self.button_index].on_deselection()
            self.button_index += 1
            self.buttons[self.button_index].on_selection()
        else:
            self.buttons[self.button_index].on_deselection()
            self.button_index = 0
            self.buttons[self.button_index].on_selection()


    def previous_button(self):
        if self.button_index > 0:
            self.buttons[self.button_index].on_deselection()
            self.button_index -= 1
            self.buttons[self.button_index].on_selection()
        else:
            self.buttons[self.button_index].on_deselection()
            self.button_index = len(self.buttons) - 1
            self.buttons[self.button_index].on_selection()
        
    def select_c_button(self):
        self.buttons[self.button_index].on_press()
        
    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)


class MainMenu:
    def __init__(self, screen_size = snake_rules.screen_size):
        x_diff = 130
        y_diff = 120
        offset = (0, 120)
        mid_point = (screen_size[0] / 2 + offset[0], screen_size[1] / 2 + offset[1])

        x_frame = (mid_point[0] - x_diff, mid_point[0] + x_diff)
        y_frame = (mid_point[1] - y_diff, mid_point[1] + y_diff)
        s_colors = [Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE, Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE,Colors.LIGHT_BLUE]
        colors = [Colors.DARK_LIGHT_BLUE,Colors.DARK_LIGHT_BLUE,Colors.DARK_LIGHT_BLUE,Colors.DARK_LIGHT_BLUE,Colors.DARK_LIGHT_BLUE, Colors.DARK_LIGHT_BLUE, Colors.DARK_LIGHT_BLUE,Colors.DARK_LIGHT_BLUE,Colors.DARK_LIGHT_BLUE,Colors.DARK_LIGHT_BLUE,Colors.DARK_LIGHT_BLUE, Colors.DARK_LIGHT_BLUE]
        text = ["Casual", "AI vs Player", "Only AI", "Learning", "Map Builder", "bababa","oppai", "AI vs Player", "Only AI", "Learning", "Map Builder", "bababa"]

        def test():
            print("this is a test")

        functions = [test, test,test,test,test,test, test, test,test,test,test,test]

        self.button_set = ButtonSet((x_frame,y_frame), 5, 5, 0, 4,1,4,text, colors, s_colors,0,functions)
       

    def update_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == snake_rules.down_key:
                self.button_set.next_button()
            if event.key == snake_rules.up_key:
                self.button_set.previous_button()
            if event.key == snake_rules.select_key:
                self.button_set.select_c_button()

    def update_logic(self):
        pass

    def draw(self, screen):
        self.button_set.draw(screen)

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
            main_menu.update_events(event)


    
        screen.fill(Colors.WHITE)
        main_menu.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
