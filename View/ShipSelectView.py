# importation for pygame, MainMenuView and View and Sprite class
import pygame
import View.MainMenuView as main
import View.GameplayView as gameplay
from View.ParentView import View, Sprite

# Ship select view controls ship select menu


class ShipSelectView(View):
    # ShipSelectView, child class of ParentView
    def __init__(self):
        super(ShipSelectView, self).__init__()
        self.name = "ShipSelect"
        self.bg = pygame.image.load('Sprites/Menu/Select_Page.png')
        self.baseShip = Sprite(310, 350, 64, self.BasicShipFrames, 0)
        # 146x44
        self.backButton = ButtonOption("back", pygame.image.load('Sprites/Options/Back.png'), pygame.image.load('Sprites/Options/Back_Highlighted.png'), 25, 675)
        self.playButton = ButtonOption("play", pygame.image.load('Sprites/Options/Play.png'), pygame.image.load('Sprites/Options/H_Play.png'), 270, 550)

    def draw(self, mouse, dt):
        # repeatedly draws the screen, must provide: (mouse position, milliseconds since last frame)
        self.screen.blit(self.bg, (0, 0))
        # pygame.draw.rect(self.screen, (255, 255, 255),
        # (self.baseShip.xcor - 20, self.baseShip.ycor - 15, 100, 100), 2)
        self.baseShip.update(self.screen, dt)
        self.display_ship_name()
        self.display_button(mouse)
        pygame.display.update()

    def display_button(self, mouse):
        # displays back button. Highlights if hovered
        if self.backButton.xAxis + 146 > mouse[0] > self.backButton.xAxis and self.backButton.yAxis + 44 > mouse[1] > self.backButton.yAxis:
            self.screen.blit(self.backButton.highlighted, (self.backButton.xAxis, self.backButton.yAxis))
            self.screen.blit(self.playButton.unhighlighted, (self.playButton.xAxis, self.playButton.yAxis))
        elif self.playButton.xAxis + 146 > mouse[0] > self.playButton.xAxis and self.playButton.yAxis + 44 > mouse[1] > self.playButton.yAxis:
            self.screen.blit(self.playButton.highlighted, (self.playButton.xAxis, self.playButton.yAxis))
            self.screen.blit(self.backButton.unhighlighted, (self.backButton.xAxis, self.backButton.yAxis))
        else:
            self.screen.blit(self.backButton.unhighlighted, (self.backButton.xAxis, self.backButton.yAxis))
            self.screen.blit(self.playButton.unhighlighted, (self.playButton.xAxis, self.playButton.yAxis))

    def click_event(self, mouse):
        # returns MainMenuView if an button is clicked. Otherwise it returns self. Must provide: (mouse position)
        if self.backButton.xAxis + 146 > mouse[0] > self.backButton.xAxis and self.backButton.yAxis + 44 > mouse[1] > self.backButton.yAxis:
            self.transition()
            return main.MainMenuView()
        if self.playButton.xAxis + 146 > mouse[0] > self.playButton.xAxis and self.playButton.yAxis + 44 > mouse[
            1] > self.playButton.yAxis:
            self.transition()
            return gameplay.GameplayView()
        else:
            return self

    def key_event(self, key):
        # returns to MainMenuView after user pushes escape. Otherwise returns self. Must provide: (key pressed)
        if key[pygame.K_ESCAPE]:
            self.transition()
            return main.MainMenuView()
        if key[pygame.K_KP_ENTER] or key[pygame.K_RETURN]:
            self.transition()
            return gameplay.GameplayView()
        else:
            return self

    def display_ship_name(self):
        pygame.font.init()
        allFonts = pygame.font.get_fonts()
        font = pygame.font.SysFont(allFonts[8], 30)
        text = font.render('Infinity', False, (255, 255, 255))
        self.screen.blit(text, (275, 450))


class ButtonOption(object):
    # button option class. (name of button, unhighlighted image of button, highlighted image of button, x axis, y axis)
    def __init__(self, name, unhighlighted, highlighted, xAxis, yAxis):
        self.name = name
        self.unhighlighted = unhighlighted
        self.highlighted = highlighted
        self.xAxis = xAxis
        self.yAxis = yAxis


