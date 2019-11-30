# importation for pygame, MainMenuView and View and Sprite class
import pygame
import View.MainMenuView as main
import View.PlayerControlView as controls
from View.ParentView import View, Sprite


# Ship select view controls ship select menu


class ShipSelectView(View):
    # ShipSelectView, child class of ParentView
    def __init__(self):
        super(ShipSelectView, self).__init__()
        self.name = "ShipSelect"
        self.bg = pygame.image.load('Sprites/Menu/Select_Page.png')
        # 146x44
        self.backButton = ButtonOption("back", pygame.image.load('Sprites/Options/Back.png'),
                                       pygame.image.load('Sprites/Options/Back_Highlighted.png'), 25, 675)
        self.playButton = ButtonOption("play", pygame.image.load('Sprites/Options/Play.png'),
                                       pygame.image.load('Sprites/Options/H_Play.png'), 270, 600)
        self.leftArrow = ButtonOption("left", pygame.image.load('Sprites/Options/Left_Arrow.png'),
                                      pygame.image.load('Sprites/Options/Left_Arrow_Highlighted.png'), 125, 350)
        self.rightArrow = ButtonOption("right", pygame.image.load('Sprites/Options/Right_Arrow.png'),
                                       pygame.image.load('Sprites/Options/Right_Arrow_Highlighted.png'), 511, 350)
        self.index = 0
        self.ships = [Ships('Infinity', Sprite(318, 350, 64, self.BasicShipFrames, 0)), Ships('Imperier', Sprite(318, 350, 64, View.load_images('Sprites/PlayerShips/Imperier/Flying'), 0)), Ships('Scatter', Sprite(318, 350, 64, View.load_images('Sprites/PlayerShips/Scatter/Flying'), 0))]

    def draw(self, mouse, dt):
        # repeatedly draws the screen, must provide: (mouse position, milliseconds since last frame)
        self.screen.blit(self.bg, (0, 0))
        # pygame.draw.rect(self.screen, (255, 255, 255),
        # (self.baseShip.xcor - 20, self.baseShip.ycor - 15, 100, 100), 2)
        self.ships[self.index].images.update(self.screen, dt)
        self.display_ship_name()
        self.display_button(mouse)
        pygame.display.update()

    def display_button(self, mouse):
        # displays back button. Highlights if hovered
        if self.backButton.xAxis + 146 > mouse[0] > self.backButton.xAxis and self.backButton.yAxis + 44 > mouse[
            1] > self.backButton.yAxis:
            self.screen.blit(self.backButton.highlighted, (self.backButton.xAxis, self.backButton.yAxis))
            self.screen.blit(self.playButton.unhighlighted, (self.playButton.xAxis, self.playButton.yAxis))
            self.screen.blit(self.leftArrow.unhighlighted, (self.leftArrow.xAxis, self.leftArrow.yAxis))
            self.screen.blit(self.rightArrow.unhighlighted, (self.rightArrow.xAxis, self.rightArrow.yAxis))
        elif self.playButton.xAxis + 146 > mouse[0] > self.playButton.xAxis and self.playButton.yAxis + 44 > mouse[
            1] > self.playButton.yAxis:
            self.screen.blit(self.playButton.highlighted, (self.playButton.xAxis, self.playButton.yAxis))
            self.screen.blit(self.backButton.unhighlighted, (self.backButton.xAxis, self.backButton.yAxis))
            self.screen.blit(self.leftArrow.unhighlighted, (self.leftArrow.xAxis, self.leftArrow.yAxis))
            self.screen.blit(self.rightArrow.unhighlighted, (self.rightArrow.xAxis, self.rightArrow.yAxis))
        elif self.leftArrow.xAxis + 64 > mouse[0] > self.leftArrow.xAxis and self.leftArrow.yAxis + 64 > mouse[
            1] > self.leftArrow.yAxis:
            self.screen.blit(self.backButton.unhighlighted, (self.backButton.xAxis, self.backButton.yAxis))
            self.screen.blit(self.playButton.unhighlighted, (self.playButton.xAxis, self.playButton.yAxis))
            self.screen.blit(self.leftArrow.highlighted, (self.leftArrow.xAxis, self.leftArrow.yAxis))
            self.screen.blit(self.rightArrow.unhighlighted, (self.rightArrow.xAxis, self.rightArrow.yAxis))
        elif self.rightArrow.xAxis + 64 > mouse[0] > self.rightArrow.xAxis and self.rightArrow.yAxis + 64 > mouse[
            1] > self.rightArrow.yAxis:
            self.screen.blit(self.backButton.unhighlighted, (self.backButton.xAxis, self.backButton.yAxis))
            self.screen.blit(self.playButton.unhighlighted, (self.playButton.xAxis, self.playButton.yAxis))
            self.screen.blit(self.leftArrow.unhighlighted, (self.leftArrow.xAxis, self.leftArrow.yAxis))
            self.screen.blit(self.rightArrow.highlighted, (self.rightArrow.xAxis, self.rightArrow.yAxis))
        else:
            self.screen.blit(self.backButton.unhighlighted, (self.backButton.xAxis, self.backButton.yAxis))
            self.screen.blit(self.playButton.unhighlighted, (self.playButton.xAxis, self.playButton.yAxis))
            self.screen.blit(self.leftArrow.unhighlighted, (self.leftArrow.xAxis, self.leftArrow.yAxis))
            self.screen.blit(self.rightArrow.unhighlighted, (self.rightArrow.xAxis, self.rightArrow.yAxis))

    def click_event(self, mouse):
        # returns MainMenuView if an button is clicked. Otherwise it returns self. Must provide: (mouse position)
        if self.backButton.xAxis + 146 > mouse[0] > self.backButton.xAxis and self.backButton.yAxis + 44 > mouse[
            1] > self.backButton.yAxis:
            self.transition()
            return main.MainMenuView()
        if self.playButton.xAxis + 146 > mouse[0] > self.playButton.xAxis and self.playButton.yAxis + 44 > mouse[
            1] > self.playButton.yAxis:
            self.transition()
            return controls.PlayerControlView()
        elif self.leftArrow.xAxis + 64 > mouse[0] > self.leftArrow.xAxis and self.leftArrow.yAxis + 64 > mouse[
            1] > self.leftArrow.yAxis:
            self.index -= 1
            if self.index < 0:
                self.index = len(self.ships) - 1
            return self
        elif self.rightArrow.xAxis + 64 > mouse[0] > self.rightArrow.xAxis and self.rightArrow.yAxis + 64 > mouse[
            1] > self.rightArrow.yAxis:
            self.index += 1
            if self.index >= len(self.ships):
                self.index = 0
            return self
        else:
            return self

    def key_event(self, key):
        # returns to MainMenuView after user pushes escape. Otherwise returns self. Must provide: (key pressed)
        if key[pygame.K_ESCAPE]:
            self.transition()
            return main.MainMenuView()
        if key[pygame.K_KP_ENTER] or key[pygame.K_RETURN]:
            self.transition()
            return controls.PlayerControlView()
        else:
            return self

    def display_ship_name(self):
        pygame.font.init()
        allFonts = pygame.font.get_fonts()
        font = pygame.font.SysFont(allFonts[8], 30)
        text = font.render(self.ships[self.index].name, False, (255, 255, 255))
        text_rect = text.get_rect(center=(self.windowWidth / 2, 450))
        self.screen.blit(text, text_rect)


class ButtonOption(object):
    # button option class. (name of button, unhighlighted image of button, highlighted image of button, x axis, y axis)
    def __init__(self, name, unhighlighted, highlighted, xAxis, yAxis):
        self.name = name
        self.unhighlighted = unhighlighted
        self.highlighted = highlighted
        self.xAxis = xAxis
        self.yAxis = yAxis


class Ships(object):
    def __init__(self, name, images):
        self.name = name
        self.images = images
