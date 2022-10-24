# pylint: disable=E1101

import pygame
from src.base import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()


def init(caption, icon):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(caption)
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    return screen, clock
