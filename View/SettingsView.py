# importation for pygame and MainMenuView and classes View and Sprite
import pygame
import View.MainMenuView as main
from View.ParentView import View, Sprite


class SettingsView(View):
    # SettingsView, child class of ParentView
    def __init__(self):
        super(SettingsView, self).__init__()
        self.name = "Settings"
        # background image
        self.bg = pygame.image.load('Sprites/Menu/Settings_Page.png')
        # creates all the sprite stars and puts it in Sprite.Group
        self.stars = self.make_stars()
        # 146x44
        self.backButton = ButtonOption("back", pygame.image.load('Sprites/Options/Back.png'), pygame.image.load('Sprites/Options/Back_Highlighted.png'), 25, 675)

    def make_stars(self):
        # creates stars for the main menu background. Returns pygame.sprite.Group() of stars
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
        # repeatedly draws the screen, must provide: (mouse position, milliseconds since last frame)
        self.screen.blit(self.bg, (0, 0))
        self.display_back(mouse)
        self.stars.update(self.screen, dt)
        self.stars.draw(self.screen)
        pygame.display.update()

    def display_back(self, mouse):
        # displays back button. Highlights if hovered
        if self.backButton.xAxis + 146 > mouse[0] > self.backButton.xAxis and self.backButton.yAxis + 44 > mouse[1] > self.backButton.yAxis:
            self.screen.blit(self.backButton.highlighted, (self.backButton.xAxis, self.backButton.yAxis))
        else:
            self.screen.blit(self.backButton.unhighlighted, (self.backButton.xAxis, self.backButton.yAxis))

    def click_event(self, mouse):
        # returns MainMenuView if an button is clicked. Otherwise it returns self. Must provide: (mouse position)
        if self.backButton.xAxis + 146 > mouse[0] > self.backButton.xAxis and self.backButton.yAxis + 44 > mouse[1] > self.backButton.yAxis:
            self.transition()
            return main.MainMenuView()
        else:
            return self

    def key_event(self, key):
        # returns to MainMenuView after user pushes escape. Otherwise returns self. Must provide: (key pressed)
        if key[pygame.K_ESCAPE]:
            self.transition()
            return main.MainMenuView()
        else:
            return self


class ButtonOption(object):
    # button option class. (name of button, unhighlighted image of button, highlighted image of button, x axis, y axis)
    def __init__(self, name, unhighlighted, highlighted, xAxis, yAxis):
        self.name = name
        self.unhighlighted = unhighlighted
        self.highlighted = highlighted
        self.xAxis = xAxis
        self.yAxis = yAxis