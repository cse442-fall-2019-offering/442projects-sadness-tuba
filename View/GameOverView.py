# importation for pygame and MainMenuView and classes View and Sprite
import pygame
import os
import View.MainMenuView as main
import View.GameplayView as gameplay
import Controller.MenuController as menu
from View.ParentView import View, Sprite


class GameOverView(View):
    # GameOverView, child class of ParentView
    def __init__(self):

        # checks if score file is in directory
        lst = [0, 0, 0, 0, 0]
        if not os.path.exists("score.txt"):
            with open("score.txt", "w+") as f:
                for i in range(5):
                    f.write(str(0) + '\n')
        else:
            with open("score.txt", "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    lst[i] = int(line.rstrip('\n'))


        super(GameOverView, self).__init__()
        self.name = "GameOver"
        self.allFonts = pygame.font.get_fonts()
        self.font = pygame.font.SysFont(self.allFonts[8], 30)
        # background image
        self.bg = pygame.image.load('Sprites/Menu/Blank_Page.png')
        # creates all the sprite stars and puts it in Sprite.Group
        self.stars = self.make_stars()
        # 146x88
        self.gameOverLabel = Label("game_over", pygame.image.load('Sprites/Options/Game_Over.png'), 146, 88) # [2] 146
        self.retry = TextOption('Retry', 305, 550) # [2] 400
        self.mainMenu = TextOption('Main Menu', 275, 600) # [2] 450

        # updates scoreboard
        with open("score.txt", "w+") as f:
            if gameplay.globalPlayerScore > min(lst):
                lst.append(gameplay.globalPlayerScore)
                lst.sort(reverse=True)
                lst.pop()
                for i in range(5):
                    f.write(str(lst[i]) + '\n')

        self.score1 = TextOption('1. ' + str(lst[0]).zfill(6),((self.windowWidth-self.gameOverLabel.xAxis)/2)-10,270)
        self.score2 = TextOption('2. ' + str(lst[1]).zfill(6),((self.windowWidth-self.gameOverLabel.xAxis)/2)-10,320)
        self.score3 = TextOption('3. ' + str(lst[2]).zfill(6),((self.windowWidth-self.gameOverLabel.xAxis)/2)-10,370)
        self.score4 = TextOption('4. ' + str(lst[3]).zfill(6),((self.windowWidth-self.gameOverLabel.xAxis)/2)-10,420)
        self.score5 = TextOption('5. ' + str(lst[4]).zfill(6),((self.windowWidth-self.gameOverLabel.xAxis)/2)-10,470)
        self.gameOver = False

    # def sortScore(self):
    #     menu.scoreFile.write(str(gameplay.globalPlayerScore))

    def make_stars(self):
        # creates stars for the main menu background. Returns pygame.sprite.Group() of stars
        starsBackground = pygame.sprite.Group()
        background = [Sprite(75, 400, 32, self.star1, 0),
                      Sprite(625, 630, 32, self.star1, 1),
                      Sprite(555, 655, 32, self.star1, 2),
                      Sprite(84, 623, 32, self.star1, 2),
                      Sprite(620, 121, 32, self.star1, 2),
                      Sprite(606, 340, 32, self.star2, 0),
                      Sprite(437, 58, 32, self.star2, 0),
                      Sprite(428, 690, 32, self.star2, 1),
                      Sprite(614, 207, 32, self.star2, 2),
                      Sprite(280, 20, 32, self.star2, 2),
                      Sprite(30, 523, 32, self.star3, 0),
                      Sprite(465, 196, 32, self.star3, 0),
                      Sprite(72, 186, 32, self.star3, 1),
                      Sprite(171, 63, 32, self.star3, 1),
                      Sprite(230, 701, 32, self.star3, 2)]
        for b in background:
            starsBackground.add(b)
        return starsBackground

    def draw(self, mouse, dt):
        # repeatedly draws the screen, must provide: (mouse position, milliseconds since last frame)
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.gameOverLabel.image, ((self.windowWidth-self.gameOverLabel.xAxis)/2, 100)) # [2] 275
        self.display_options(self.retry, mouse)
        self.display_options(self.mainMenu, mouse)
        self.display_options(self.score1, mouse)
        self.display_options(self.score2, mouse)
        self.display_options(self.score3, mouse)
        self.display_options(self.score4, mouse)
        self.display_options(self.score5, mouse)
        self.stars.update(self.screen, dt)
        self.stars.draw(self.screen)
        pygame.display.update()

    def display_options(self, option, mouse):
        # displays back button. Highlights if hovered
        text = self.font.render(option.name, False, (169, 169, 169))
        if option.xAxis + 160 > mouse[0] > option.xAxis and option.yAxis + 30 > mouse[1] > option.yAxis:
            text = self.font.render(option.name, False, (255, 255, 255))
            self.screen.blit(text, (option.xAxis, option.yAxis))
        else:
            self.screen.blit(text, (option.xAxis, option.yAxis))

    def click_event(self, mouse):
        # returns MainMenuView if an button is clicked. Otherwise it returns self. Must provide: (mouse position)
        if 435 > mouse[0] > 275 and self.retry.yAxis + 30 > mouse[1] > self.retry.yAxis:
            self.transition()
            return gameplay.GameplayView()
        elif 435 > mouse[0] > 275 and self.mainMenu.yAxis + 30 > mouse[1] > self.mainMenu.yAxis:
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


class Label(object):
    # game over label
    def __init__(self, name, image, xAxis, yAxis):
        self.name = name
        self.image = image
        self.xAxis = xAxis
        self.yAxis = yAxis


class TextOption(object):
    def __init__(self, name, xAxis, yAxis):
        self.name = name
        self.xAxis = xAxis
        self.yAxis = yAxis