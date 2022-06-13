import pygame
import pygame_gui
import better_rect
import snake_rules
import MathHelper as op
import Colors


class MouseEvents():
    def __init__(self, dimensions = snake_rules.screen_size):
        self.dimensions = dimensions
        self.offset = op.divide_vector(dimensions,2)
        self.last_mouse_state = None
        self.current_mouse_state = None


    def update(self, delta_time):
        self.last_mouse_state = self.current_mouse_state
        self.current_mouse_state = [pygame.mouse.get_focused(), pygame.mouse.get_pos(), pygame.mouse.get_pressed()]

    





    


class MapBuilder():
    def __init__(self, dimensions = snake_rules.screen_size):
        self.dimensions = dimensions
        self.offset = (0, 0)
        self.tiles = []
        self.zoom = 2
        # defines what the user can do in the current moment -- starttool = freeflow
        self.tool = "free_flow"
        self.zoom_multiplier = 0.5
        self.min_zoom = 0.5
        self.max_zoom = 3
        self.l_mouse_pos = None
        self.c_mouse_pos = None
        self.s_m_offset = None
        #self.display = pygame.surface(int(dimensions[0] / self.zoom), int(dimensions[1]/ self.zoom))

        x = (int)(self.dimensions[0] / snake_rules.pixel_size[0])
        y = (int)(self.dimensions[1] / snake_rules.pixel_size[1])

        for x_p in range(x * 2):
            for y_p in range(y * 2):
                self.tiles.append(ClickableTile(snake_rules.multiply_vectors((x_p, y_p), snake_rules.pixel_size), snake_rules.pixel_size))

    def draw(self, screen):
            for tile in self.tiles:

                tile.draw(screen)

    def update_events(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.trigger_zoom(event.y)

    def trigger_zoom(self, y):
        if y > 0:
            if self.zoom < self.max_zoom:
                self.zoom += y * self.zoom_multiplier
        else:
            if self.zoom > self.min_zoom:
                self.zoom += y * self.zoom_multiplier
        
        
        if self.zoom > self.max_zoom:
            self.zoom = self.max_zoom
        if self.zoom < self.min_zoom:
            self.zoom = self.min_zoom

        if self.zoom == self.max_zoom or self.zoom == self.min_zoom:
            return None
        else:
            for tile in self.tiles:
                tile.zoom(self.zoom)



    def update(self, delta_time):
        self.l_mouse_pos = self.c_mouse_pos
        self.c_mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            d_m_movement = op.subtract_vectors(self.c_mouse_pos, self.l_mouse_pos)
            self.offset = op.add_vectors(self.offset, d_m_movement)


        for tile in self.tiles:
            tile.set_offset(self.offset)
            tile.selection_check(self.c_mouse_pos)
    
class ClickableTile(better_rect.OutlinedSurface):
    def __init__(self, position, size, color=Colors.WHITE, outline_color=Colors.BLACK, outline_width=2):
        super().__init__(position, size, color, outline_color, outline_width)
        self.origin_size = self.t_size
        self.current_offset = (0, 0)

        self.origin_pos = self.t_position
        self.zoom_multiplier = 1
    
    def zoom(self, zoom):
        self.set_size(snake_rules.multiply_vector(self.origin_size, zoom))
        self.set_position(snake_rules.subtract_vectors(snake_rules.multiply_vector(self.origin_pos, zoom),self.current_offset))
        self.zoom_multiplier = zoom
    
    def set_offset(self, offset):
        self.current_offset = offset
        self.set_position(snake_rules.add_vectors(snake_rules.multiply_vector(self.origin_pos, self.zoom_multiplier),self.current_offset))

    def on_hover(self):
        self.set_color(Colors.BACKGROUND_GRAY)
        self.o_width = 3
        self.set_outline_color(Colors.mix_colors(Colors.BACKGROUND_GRAY, Colors.BLACK))
        
    def on_deselection(self):
        self.set_color(Colors.WHITE)
        self.set_outline_color(Colors.BLACK)

    def selection_check(self, position):
        if pygame.Rect.collidepoint(self.get_outer_rect(),position):
            self.on_hover()
        else:
            self.on_deselection()
        




pygame.init()

quit = False

map_builder = MapBuilder()
screen = pygame.display.set_mode(map_builder.dimensions)
pygame.display.set_caption("Builder Tool")
clock = pygame.time.Clock()
ticks_last_frame = 0

while not quit:

    t = pygame.time.get_ticks()
    delta_time = (t - ticks_last_frame) / 1000.0
    ticks_last_frame = t

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True    
        map_builder.update_events(event)

    map_builder.update(delta_time)
    screen.fill(Colors.BACKGROUND_GRAY)
    map_builder.draw(screen)
    pygame.display.flip()

    clock.tick(snake_rules.f_rate)
