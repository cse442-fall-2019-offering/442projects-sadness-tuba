import pygame  # importation for pygame

import os

import Model

from Model import optionTuple, backOption, AnimatedBackgroundSprite, PlayerShip

# Pygame window width
winWidth = 700

# Pygame window height
widHeight = 750

# Height of each menu option image
optionHeight = 44

# Spacing between each Menu option image
heightSpacing = 75

smallSize = 32

mediumSize = 64

animationTime = .08

FPS = 60

clock = pygame.time.Clock()

# displays screen with specified window width and window height
win = pygame.display.set_mode((winWidth, widHeight))

# Initialize the background image
bg = pygame.image.load('Menu/Main_Menu.png')
settingsbg = pygame.image.load('Menu/Settings_Page.png')
blankbg = pygame.image.load('Menu/Blank_Page.png')
# used to display name of window at the top
pygame.display.set_caption('BEYOND INFINITY')

# Sets the icon for the game
iconimage = pygame.image.load('PlayerShips/BasicShipFlying0.png')
pygame.display.set_icon(iconimage)


# Loads all images in directory. The directory must only contain images.

def load_images(path):
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name).convert()
        images.append(image)
    return images


# Frames for playership
BasicShipFrames = load_images('PlayerShips')
# Frames for stars
Star1 = load_images('Background/Animated_Star1')

Star2 = load_images('Background/Animated_Star2')

Star3 = load_images('Background/Animated_Star3')
# creates the player object
player = PlayerShip(100, 350, BasicShipFrames, mediumSize, mediumSize, animationTime, 0)

background = [AnimatedBackgroundSprite(75, 400, Star1, smallSize, animationTime, 0),
              AnimatedBackgroundSprite(625, 630, Star1, smallSize, animationTime, 1),
              AnimatedBackgroundSprite(355, 655, Star1, smallSize, animationTime, 2),
              AnimatedBackgroundSprite(84, 623, Star1, smallSize, animationTime, 2),
              AnimatedBackgroundSprite(606, 340, Star2, smallSize, animationTime, 0),
              AnimatedBackgroundSprite(428, 690, Star2, smallSize, animationTime, 1),
              AnimatedBackgroundSprite(250, 300, Star2, smallSize, animationTime, 2),
              AnimatedBackgroundSprite(163, 534, Star2, smallSize, animationTime, 2),
              AnimatedBackgroundSprite(552, 458, Star3, smallSize, animationTime, 0),
              AnimatedBackgroundSprite(512, 594, Star3, smallSize, animationTime, 0),
              AnimatedBackgroundSprite(252, 700, Star3, smallSize, animationTime, 1),
              AnimatedBackgroundSprite(482, 310, Star3, smallSize, animationTime, 2)]


# This definition draws the options onto the pygame window


def create_options(option, mouse):
    width_spacing = ((winWidth - option.imgWidth) / 2)
    if Model.selectedOption.name == option.name:
        win.blit(option.highlighted, (width_spacing, option.yAxisImageSpacing))
    elif width_spacing + option.imgWidth > mouse[0] > width_spacing and option.yAxisImageSpacing + optionHeight > mouse[
        1] > option.yAxisImageSpacing:
        win.blit(option.highlighted, (width_spacing, option.yAxisImageSpacing))
        Model.selectedOption = option
        player.ycor = option.yAxisImageSpacing
        player.xcor = width_spacing - 77
    else:
        win.blit(option.unhighlighted, (width_spacing, option.yAxisImageSpacing))


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def button(buttonName, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(win, ac, (x, y, w, h))

        # print(click)
        # if click[0] == 1 and action != None:
        #      if action == "back":
        #          1 == 1
    else:
        pygame.draw.rect(win, ic, (x, y, w, h))
    all_fonts = pygame.font.get_fonts()
    smallText = pygame.font.SysFont(all_fonts[8], 20)
    textSurf, textRect = text_objects(buttonName, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    win.blit(textSurf, textRect)


# This definition draws the background, player and also updates pygame screen show everything displays onto the window
def drawMainWindow(mouse, dt, sprite_group, playerShip):
    # Displays Menu
    win.blit(bg, (0, 0))
    sprite_group.update(dt)
    sprite_group.draw(win)
    playerShip.update(dt, win)
    for j in optionTuple:
        create_options(j, mouse)
    pygame.display.update()


def transition(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 75):
        fade.set_alpha(alpha)
        win.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(2)


def drawSettingsWindow(mouse):
    win.blit(settingsbg, (0, 0))
    #button("Back", 50, 650, 150, 50, (200, 200, 200), (100, 100, 100), "back")
    create_options(backOption, mouse)
    pygame.display.update()

def drawBlankWindow(mouse):
    win.blit(blankbg, (0, 0))
    #button("Back", 50, 650, 150, 50, (200, 200, 200), (100, 100, 100), "back")
    create_options(backOption, mouse)
    pygame.display.update()
