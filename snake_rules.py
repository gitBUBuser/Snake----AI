import pygame


screen_size = (720, 504)
snake_UI_height = 150
pixel_size = (24, 24)
step = (24, 24)


up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)


left_key = pygame.K_a
right_key = pygame.K_d
up_key = pygame.K_w
down_key = pygame.K_s
select_key = pygame.K_RETURN

f_step_interval = 3
f_rate = 60

def dir_to_string(direction):
    step_x = step[0]
    if direction == multiply_vector(up, 24):
        return "up"
    if direction == multiply_vector(down, 24):
        return "down"
    if direction == multiply_vector(left,24):
        return "left"
    if direction == multiply_vector(right,24):
        return "right"

def string_to_dir(dir_string):
    if dir_string == "up":
        return up
    if dir_string == "down":
        return down
    if dir_string == "left":
        return left
    if dir_string == "right":
        return right


def add_vectors(a = (0,0), b = (0,0)):
    if type(a) == tuple and type(b) == tuple:
        return (a[0] + b[0], a[1] + b[1])
    else:
        return "failed, wrong type"

def subtract_vectors(a = (0,0), b = (0,0)):
    if type(a) == tuple and type(b) == tuple:
        return (a[0] - b[0], a[1] - b[1])
    else:
        return "failed, wrong type"

def multiply_vectors(a = (0,0), b = (0,0)):
    if type(a) == tuple and type(b) == tuple:
        return (a[0] * b[0], a[1] * b[1])
    else:
         return "failed, wrong type"


def multiply_vector(a = (0,0), b = 0):
    return (a[0] * b, a[1] * b)
    