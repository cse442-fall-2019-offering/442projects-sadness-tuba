import pygame  # importation for pygame


class MenuOption(object):

    def __init__(self, name, unhighlighted, highlighted, imgWidth, yAxisImageSpacing):
        self.name = name
        self.unhighlighted = unhighlighted
        self.highlighted = highlighted
        self.imgWidth = imgWidth
        self.yAxisImageSpacing = yAxisImageSpacing


#  option class (button name, image, highlighted image, image width, height spacing between each image)
#  If you want to add one more option, add 75 to height spacing between each image
# 346x44
startOption = MenuOption("start", pygame.image.load('../Options/Start_Game.png'), pygame.image.load('../Options/Start_Game_Highlighted.png'), 346, 0)
# 146x44
shopOption = MenuOption("shop", pygame.image.load('../Options/Shop.png'), pygame.image.load('../Options/Shop_Highlighted.png'), 146, 0)
# 274x44
settingsOption = MenuOption("settings", pygame.image.load('../Options/Settings.png'), pygame.image.load('../Options/Settings_Highlighted.png'), 274, 0)
# 126x44
quitOption = MenuOption("quit", pygame.image.load('../Options/Quit.png'), pygame.image.load('../Options/Quit_Highlighted.png'), 126, 0)
# Selected option is the  option the user has selected. This will be used to determine when the image becomes
# highlighted
selectedOption = startOption

# a tuple that stores all the men option tuples
optionTuple = (startOption, shopOption, settingsOption, quitOption)

class PlayerShip(object):
    # Need to initialize class by defining its properties
    def __init__(self, xcor, ycor, width, height, shipFrames):
        self.xcor = xcor
        self.ycor = ycor
        self.width = width
        self.height = height
        self.shipFrames = shipFrames
        self.ShipFrame = 0
    # Used to draw the player ship onto the pygame window

    def draw(self, window):
        self.ShipFrame += 1
        if self.ShipFrame == len(self.shipFrames) - 1:
            self.ShipFrame = 1
        window.blit(self.shipFrames[self.ShipFrame - 1], (self.xcor, self.ycor))
