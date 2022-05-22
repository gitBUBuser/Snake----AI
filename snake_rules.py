import pygame

screen_size = (704, 512)
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

f_step_interval = 4


def add_vectors(a = (0,0), b = (0,0)):
    if type(a) == tuple and type(b) == tuple:
        return (a[0] + b[0], a[1] + b[1])
    else:
        return "failed, wrong type"

def multiply_vectors(a = (0,0), b = (0,0)):
    if type(a) == tuple and type(b) == tuple:
        return (a[0] * b[0], a[1] * b[1])
    else:
         return "failed, wrong type"


   
    