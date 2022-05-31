from cmath import rect
from turtle import color, shape
from unicodedata import name
import pygame
import snake_rules
import Colors
import pygame_gui
import pygame_gui.elements as ui_elements
import UI_extras


class SnakeScore():
    def __init__(self,container, ui_manager, relative_rect, score = 1, snake_name = "sneaktSHEI"):
        self.score = score
        self.time = 0
        self.container = container
        self.relative_rect = relative_rect
        self.ui_manager = ui_manager
        self.name = snake_name

        self.text = ui_elements.UILabel(
            container=self.container,
            relative_rect=self.relative_rect,
            text=str(self.name + ": " + str(self.score)),
            manager= self.ui_manager
        )
        
    def update_score(self, new_score):
        self.score = new_score
        self.text.set_text(str(self.name + ": " + str(self.score)))


class SnakeUI():
    def __init__(self, position, ui_manager, size, snake):
        self.position = position
        self.ui_manager = ui_manager
        self.size = size
        self.snake = snake

        self.back_panel = ui_elements.UIPanel(
            relative_rect=pygame.Rect((self.position),(self.size)),
            starting_layer_height=0,
            manager=self.ui_manager
        )
        
        self.profile_panel = ui_elements.UIPanel(
            container=self.back_panel,
            relative_rect=pygame.Rect(self.back_panel.relative_rect.width * 0.05, (self.back_panel.relative_rect.height * 0.25) - (self.back_panel.relative_rect.height * 0.8 * 0.25), self.back_panel.relative_rect.height * 0.8,self.back_panel.relative_rect.height * 0.8),
            starting_layer_height=3,
            manager=self.ui_manager
        )

        self.snake_name_panel = ui_elements.UIPanel(
            container=self.back_panel,
            starting_layer_height=1,
            relative_rect=pygame.Rect(self.profile_panel.relative_rect.width * 0.8 + self.profile_panel.relative_rect.x, self.back_panel.relative_rect.height * 0.125,  self.back_panel.relative_rect.width * 0.6,self.back_panel.relative_rect.height * 0.3),
            manager=self.ui_manager
        )

        self.snake_score_panel = ui_elements.UIPanel(
            container=self.back_panel,
            starting_layer_height=1,
            relative_rect=pygame.Rect(self.profile_panel.relative_rect.width * 0.8 + self.profile_panel.relative_rect.x, self.back_panel.relative_rect.height * 0.4,  self.back_panel.relative_rect.width * 0.45,self.back_panel.relative_rect.height * 0.4),
            manager=self.ui_manager
        )

        self.score_text = SnakeScore(self.snake_score_panel, self.ui_manager, pygame.Rect((10,0),(100,35)),snake_name="Score")
        self.s_name_string = ui_elements.UILabel(
            container = self.snake_name_panel,
            relative_rect=pygame.Rect((10,0),(100,35)),
            text="SneakySnake",
            manager=self.ui_manager
        )
    
    def set_score(self, new_score):
        self.score_text.update_score(new_score)
    

class UserInterface():
    def __init__(self, resolution):
        
        self.size = resolution
        self.snake_interfaces = []
        self.color = Colors.UI_Color
        self.score = 1
        self.time = 0

        self.window_surface = pygame.display.set_mode(self.size)
        self.ui_manager = pygame_gui.UIManager(self.size)
        self.ui_manager.get_theme().load_theme("theme.json")
       

    def add_snake_UI(self, position, size, snake = None):
        snek_ui = SnakeUI(position, self.ui_manager, size, snake)
        self.snake_interfaces.append(snek_ui)

    def set_score(self, new_score, snake):
        for interface in self.snake_interfaces:
            if snake == interface.snake:
                interface.set_score(new_score)

    def draw(self, screen):
        self.ui_manager.draw_ui(self.window_surface)

    def update(self, tick):
        self.time += tick
        self.ui_manager.update(tick)
        #self.time_label.set_text(str(int(self.time)))
    
    def update_events(self, event):
        self.ui_manager.process_events(event)
