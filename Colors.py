
from re import template


BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
LIGHT_BLUE =  (0, 255, 255)
DARK_LIGHT_BLUE = (0, 204, 255)
DEEP_PURPLE =  (142, 68, 173)
AMNIENT_GREEN = (20, 143, 119)
SOFT_RED =  (231, 76, 60)

BACKGROUND_GRAY =  (52, 73, 94)




def mix_colors(color_1, color_2):
    temp_list = []
    if len(color_1) == len(color_2):
        for i in range(len(color_1)):
            temp_list.append((color_1[i] + color_2[i]) / 2)
        return tuple(temp_list)
    else:
        return "Error! Colors are not of the same type"

    