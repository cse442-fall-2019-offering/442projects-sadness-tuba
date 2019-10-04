import pygame  # importation for pygame
import View.MainMenuView as main

from View.ParentView import View, Sprite


class SettingsView(View):
    def __init__(self):
        super(SettingsView, self).__init__()
        self.bg = pygame.image.load('Menu/Settings_Page.png')
        self.soundEffectVolume = 0.5
        self.musicVolume = 0.5
        self.stars = self.make_stars()
        # 146x44
        self.backButton = BackOption("back", pygame.image.load('Options/Back.png'), pygame.image.load('Options/Back_Highlighted.png'), 25, 675)

    def make_stars(self):
        starsBackground = pygame.sprite.Group()
        background = [Sprite(75, 400, 32, self.star1, 0),
                      Sprite(625, 630, 32, self.star1, 1),
                      Sprite(355, 655, 32, self.star1, 2),
                      Sprite(84, 623, 32, self.star1, 2),
                      Sprite(606, 340, 32, self.star2, 0),
                      Sprite(428, 690, 32, self.star2, 1),
                      Sprite(614, 207, 32, self.star2, 2),
                      Sprite(280, 164, 32, self.star2, 2),
                      Sprite(30, 523, 32, self.star3, 0),
                      Sprite(465, 196, 32, self.star3, 0),
                      Sprite(72, 186, 32, self.star3, 1),
                      Sprite(230, 701, 32, self.star3, 2)]
        for b in background:
            starsBackground.add(b)
        return starsBackground

    def draw(self, mouse, dt):
        self.screen.blit(self.bg, (0, 0))
        self.display_back(mouse)
        self.stars.update(self.screen, dt)
        self.stars.draw(self.screen)
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