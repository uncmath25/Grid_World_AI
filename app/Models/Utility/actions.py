import pygame


class Actions():

    MOVE_NONE = 'Stay'
    MOVE_LEFT = 'Move Left'
    MOVE_RIGHT = 'Move Right'
    MOVE_UP = 'Move Up'
    MOVE_DOWN = 'Move Down'

    Map = {}
    Map[pygame.K_LEFT] = MOVE_LEFT
    Map[pygame.K_RIGHT] = MOVE_RIGHT
    Map[pygame.K_UP] = MOVE_UP
    Map[pygame.K_DOWN] = MOVE_DOWN
    Map[pygame.K_a] = MOVE_LEFT
    Map[pygame.K_d] = MOVE_RIGHT
    Map[pygame.K_w] = MOVE_UP
    Map[pygame.K_s] = MOVE_DOWN
