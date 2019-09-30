import pygame  # importation for pygame
import View.MainMenuView as main

from View.ParentView import View


class ShipSelectView(View):
    def __init__(self):
        super(ShipSelectView, self).__init__()
        self.bg = pygame.image.load('Menu/Blank_Page.png')
        # 146x44
        self.backButton = BackOption("back", pygame.image.load('Options/Back.png'), pygame.image.load('Options/Back_Highlighted.png'), 25, 675)

    def draw(self, mouse, dt):
        self.screen.blit(self.bg, (0, 0))
        self.display_back(mouse)
        pygame.display.update()

    def display_back(self, mouse):
        if self.backButton.xAxis + 146 > mouse[0] > self.backButton.xAxis and self.backButton.yAxis + 44 > mouse[1] > self.backButton.yAxis:
            self.screen.blit(self.backButton.highlighted, (self.backButton.xAxis, self.backButton.yAxis))
        else:
            self.screen.blit(self.backButton.unhighlighted, (self.backButton.xAxis, self.backButton.yAxis))

    def click_event(self, mouse):
        if self.backButton.xAxis + 146 > mouse[0] > self.backButton.xAxis and self.backButton.yAxis + 44 > mouse[1] > self.backButton.yAxis:
            self.transition()
            return main.MainMenuView()
        else:
            return self

    def key_event(self, key):
        if key[pygame.K_ESCAPE]:
            self.transition()
            return main.MainMenuView()
        else:
            return self

class BackOption(object):
    def __init__(self, name, unhighlighted, highlighted, xAxis, yAxis):
        self.name = name
        self.unhighlighted = unhighlighted
        self.highlighted = highlighted
        self.xAxis = xAxis
        self.yAxis = yAxis