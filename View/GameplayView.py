import pygame  # importation for pygame
import View.MainMenuView as main

from View.ParentView import View, Sprite


class GameplayView(View):
    def __init__(self):
        super(GameplayView, self).__init__()
        self.bg = pygame.image.load('Menu/Blank_Page.png')