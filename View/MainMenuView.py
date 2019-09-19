import pygame  # importation for pygame

import Model

from Model import PlayerShip, optionTuple

# Pygame window width
winWidth = 700

# Pygame window height
widHeight = 750

# Height of each menu option image
optionHeight = 44

# Used to rotate through the star picture frames
currentStarFrame = 0

currentStarFrame1 = 1

currentStarFrame2 = 2

# Spacing between each Menu option image
heightSpacing = 75


# displays screen with specified window width and window height
win = pygame.display.set_mode((winWidth, widHeight))

# Initialize the background image
bg = pygame.image.load('../Menu/Main_Menu.png')
# used to display name of window at the top
pygame.display.set_caption('BEYOND INFINITY')

# Frames for stars
Star1 = [pygame.image.load('../Background/Animated_Star1/Star0.png'), pygame.image.load('../Background/Animated_Star1/Star1.png'),
                   pygame.image.load('../Background/Animated_Star1/Star2.png')]

Star2 = [pygame.image.load('../Background/Animated_Star2/Star0.png'), pygame.image.load('../Background/Animated_Star2/Star1.png'),
                   pygame.image.load('../Background/Animated_Star2/Star2.png')]

Star3 = [pygame.image.load('../Background/Animated_Star3/Star0.png'), pygame.image.load('../Background/Animated_Star3/Star1.png'),
                   pygame.image.load('../Background/Animated_Star3/Star2.png')]

# Frames for playership
BasicShipFrame = [pygame.image.load('../PlayerShips/BasicShipFlying0.png'),pygame.image.load('../PlayerShips/BasicShipFlying1.png'),
               pygame.image.load('../PlayerShips/BasicShipFlying2.png'), pygame.image.load('../PlayerShips/BasicShipFlying3.png'),
               pygame.image.load('../PlayerShips/BasicShipFlying4.png'), pygame.image.load('../PlayerShips/BasicShipFlying5.png')]

# Cycles through the frames for the star images

# creates the player object
player = PlayerShip(100, 351, 64, 64, BasicShipFrame)

def make_background():
    global currentStarFrame, currentStarFrame1, currentStarFrame2
    if currentStarFrame == 3:
        currentStarFrame = 0
    if currentStarFrame1 == 3:
        currentStarFrame1 = 0
    if currentStarFrame2 == 3:
        currentStarFrame2 = 0
    win.blit(Star1[currentStarFrame], (75, 400))
    win.blit(Star1[currentStarFrame1], (625, 630))
    win.blit(Star1[currentStarFrame2], (355, 655))
    win.blit(Star1[currentStarFrame2], (84, 623))
    win.blit(Star2[currentStarFrame], (606, 340))
    win.blit(Star2[currentStarFrame1], (428, 690))
    win.blit(Star2[currentStarFrame2], (250, 300))
    win.blit(Star2[currentStarFrame2], (163, 534))
    win.blit(Star3[currentStarFrame], (552, 458))
    win.blit(Star3[currentStarFrame], (512, 594))
    win.blit(Star3[currentStarFrame1], (252, 700))
    win.blit(Star3[currentStarFrame2], (482, 310))
    currentStarFrame += 1
    currentStarFrame1 += 1
    currentStarFrame2 += 1

# This definition draws the options onto the pygame window


def create_options(option, mouse):
    width_spacing = ((winWidth - option.imgWidth) / 2)
    if Model.selectedOption.name == option.name:
        win.blit(option.highlighted, (width_spacing, option.yAxisImageSpacing))
    elif width_spacing + option.imgWidth > mouse[0] > width_spacing and option.yAxisImageSpacing + optionHeight > mouse[1] > option.yAxisImageSpacing:
        win.blit(option.highlighted, (width_spacing, option.yAxisImageSpacing))
        Model.selectedOption = option
        player.ycor = option.yAxisImageSpacing
        player.xcor = width_spacing - 77
    else:
        win.blit(option.unhighlighted, (width_spacing, option.yAxisImageSpacing))

# This defnition draws the background, player and also updates pygame screen show everything displays onto the window


def drawgamewindow(mouse):
    # Displays Menu
    win.blit(bg, (0, 0))
    make_background()
    player.draw(win)
    for j in optionTuple:
        create_options(j, mouse)
    pygame.display.update()