import pygame  # importation for pygame
from View.ParentView import View, Sprite
import View.ShipSelectView as ssv
import View.SettingsView as settings
import View.QuitView as quit


class MainMenuView(View):
    def __init__(self):
        super(MainMenuView, self).__init__()
        # Height of each menu option image
        self.optionHeight = 44
        # Spacing between each Menu option image
        self.heightSpacing = 75
        self.bg = pygame.image.load('Menu/Main_Menu.png')
        self.stars = self.make_stars()
        self.optionTuple = self.make_menu_options()
        self.ship = Sprite(100, 375, 64, self.BasicShipFrames, 0)
        self.selectedOption = self.optionTuple[0]

    def make_menu_options(self):
        #  option class (button name, image, highlighted image, image width, yaxis)
        #  If you want to add one more option, add 75 to height spacing between each image
        # 346x44
        startOption = MenuOption("start", pygame.image.load('Options/Start_Game.png'),
                                 pygame.image.load('Options/Start_Game_Highlighted.png'), 346, 375)
        # 274x44
        settingsOption = MenuOption("settings", pygame.image.load('Options/Settings.png'),
                                    pygame.image.load('Options/Settings_Highlighted.png'), 274, 450)
        # 126x44
        quitOption = MenuOption("quit", pygame.image.load('Options/Quit.png'),
                                pygame.image.load('Options/Quit_Highlighted.png'), 126, 525)
        option_tuple = (startOption, settingsOption, quitOption)
        return option_tuple

    def make_stars(self):
        starsBackground = pygame.sprite.Group()
        background = [Sprite(75, 400, 32, self.star1, 0),
                      Sprite(625, 630, 32, self.star1, 1),
                      Sprite(355, 655, 32, self.star1, 2),
                      Sprite(84, 623, 32, self.star1, 2),
                      Sprite(606, 340, 32, self.star2, 0),
                      Sprite(428, 690, 32, self.star2, 1),
                      Sprite(250, 300, 32, self.star2, 2),
                      Sprite(163, 534, 32, self.star2, 2),
                      Sprite(552, 458, 32, self.star3, 0),
                      Sprite(512, 594, 32, self.star3, 0),
                      Sprite(252, 700, 32, self.star3, 1),
                      Sprite(482, 310, 32, self.star3, 2)]
        for b in background:
            starsBackground.add(b)
        return starsBackground

    def draw(self, mouse, dt):
        self.screen.blit(self.bg, (0, 0))
        self.stars.update(self.screen, dt)
        self.stars.draw(self.screen)
        self.ship.update(self.screen, dt)
        for i in self.optionTuple:
            self.display_options(i, mouse)
        pygame.display.update()

    def click_event(self, mouse):
        for option in self.optionTuple:
            width_spacing = ((self.winWidth - option.imgWidth) / 2)
            if width_spacing + option.imgWidth > mouse[0] > width_spacing and option.yAxis + self.optionHeight > \
                    mouse[
                        1] > option.yAxis:
                self.transition()
                if self.selectedOption.name == "start":
                    return ssv.ShipSelectView()
                elif self.selectedOption.name == "settings":
                    return settings.SettingsView()
                elif self.selectedOption.name == "quit":
                    return quit.QuitView()
        return self

    def key_event(self, key):
        if key[pygame.K_DOWN]:
            for i in self.optionTuple:
                if i.name == self.selectedOption.name:
                    for idx, item in enumerate(self.optionTuple):
                        if self.selectedOption == item and idx < len(self.optionTuple) - 1:
                            self.selectedOption = self.optionTuple[idx + 1]
                            break
                        elif self.selectedOption == item and idx + 1 > len(self.optionTuple) - 1:
                            self.selectedOption = self.optionTuple[0]
                            break
                    self.ship.ycor = self.selectedOption.yAxis
                    width_spacing = ((self.winWidth - self.selectedOption.imgWidth) / 2)
                    self.ship.xcor = width_spacing - 77
                    break
            return self
        elif key[pygame.K_UP]:
            for i in self.optionTuple:
                if i.name == self.selectedOption.name:
                    for idx, item in enumerate(self.optionTuple):
                        if self.selectedOption == item and idx != 0:
                            self.selectedOption = self.optionTuple[idx - 1]
                            break
                        elif self.selectedOption == item and idx == 0:
                            self.selectedOption = self.optionTuple[len(self.optionTuple) - 1]
                            break
                    self.ship.ycor = self.selectedOption.yAxis
                    width_spacing = ((self.winWidth - self.selectedOption.imgWidth) / 2)
                    self.ship.xcor = width_spacing - 77
                    break
            return self
        elif key[pygame.K_KP_ENTER] or key[pygame.K_RETURN]:
            self.transition()
            if self.selectedOption.name == "quit":
                return quit.QuitView()
            elif self.selectedOption.name == "settings":
                return settings.SettingsView()
            elif self.selectedOption.name == "start":
                return ssv.ShipSelectView()
        else:
            return self


    def display_options(self, option, mouse):
        width_spacing = ((self.winWidth - option.imgWidth) / 2)
        if self.selectedOption.name == option.name:
            self.screen.blit(option.highlighted, (width_spacing, option.yAxis))
        elif width_spacing + option.imgWidth > mouse[0] > width_spacing and option.yAxis + self.optionHeight > \
                mouse[
                    1] > option.yAxis:
            self.screen.blit(option.highlighted, (width_spacing, option.yAxis))
            self.selectedOption = option
            self.ship.ycor = option.yAxis
            self.ship.xcor = width_spacing - 77
        else:
            self.screen.blit(option.unhighlighted, (width_spacing, option.yAxis))


class MenuOption(object):
    def __init__(self, name, unhighlighted, highlighted, imgWidth, yAxis):
        self.name = name
        self.unhighlighted = unhighlighted
        self.highlighted = highlighted
        self.imgWidth = imgWidth
        self.yAxis = yAxis
