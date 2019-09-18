import pygame  # importation for pygame

pygame.init()  # need to initialize pygame before using

clock = pygame.time.Clock()
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

# count for key pressing logic
count = 0

# displays screen with specified window width and window height
win = pygame.display.set_mode((winWidth, widHeight))


#  option array (button name, image, highlighted image, image width, height spacing between each image)
#  If you want to add one more option, add 75 to height spacing between each image

# tuple for start menu option
startOption = ("start", pygame.image.load('Options/Start_Game.png'), pygame.image.load('Options/Start_Game_Highlighted.png'), 346, 350)  # 346x44

# tuple for shop menu option
shopOption = ("shop", pygame.image.load('Options/Shop.png'), pygame.image.load('Options/Shop_Highlighted.png'), 146, 425)  # 146x44

# tuple for settings menu option
settingsOption = ("settings", pygame.image.load('Options/Settings.png'), pygame.image.load('Options/Settings_Highlighted.png'), 274, 500)  # 274x44

# tuple for quit menu option
quitOption = ("quit", pygame.image.load('Options/Quit.png'), pygame.image.load('Options/Quit_Highlighted.png'), 126, 575)  # 126x44

# Selected option is the  option the user has selected. This will be used to determine when the image becomes
# highlighted
selectedOption = startOption

# a tuple that stores all the men option tuples
optionTuple = (startOption, shopOption, settingsOption, quitOption)

# Use for determining which option gets highlighted when uses keyboard pressed
commandOptionArray = []
for z in optionTuple:
    commandOptionArray.append(z[0])

# Initialize the background image
bg = pygame.image.load('Menu/Main_Menu.png')
# used to display name of window at the top
pygame.display.set_caption('BEYOND INFINITY')

# Frames for stars
Star1 = [pygame.image.load('Background/Animated_Star1/Star0.png'), pygame.image.load('Background/Animated_Star1/Star1.png'),
                   pygame.image.load('Background/Animated_Star1/Star2.png')]

Star2 = [pygame.image.load('Background/Animated_Star2/Star0.png'), pygame.image.load('Background/Animated_Star2/Star1.png'),
                   pygame.image.load('Background/Animated_Star2/Star2.png')]

Star3 = [pygame.image.load('Background/Animated_Star3/Star0.png'), pygame.image.load('Background/Animated_Star3/Star1.png'),
                   pygame.image.load('Background/Animated_Star3/Star2.png')]

# Frames for playership
BasicShipFrame = [pygame.image.load('PlayerShips/BasicShipFlying0.png'),pygame.image.load('PlayerShips/BasicShipFlying1.png'),
               pygame.image.load('PlayerShips/BasicShipFlying2.png'), pygame.image.load('PlayerShips/BasicShipFlying3.png'),
               pygame.image.load('PlayerShips/BasicShipFlying4.png'), pygame.image.load('PlayerShips/BasicShipFlying5.png')]
# Definition to draw game window

# Class for defining the players ships so we can control its x,y coordinates


class PlayerShip(object):
    # Need to initialize class by defining its properties
    def __init__(self, xcor, ycor, width, height):
        self.xcor = xcor
        self.ycor = ycor
        self.width = width
        self.height = height
        self.ShipFrame = 0
    # Used to draw the player ship onto the pygame window

    def draw(self, window):
        self.ShipFrame += 1
        if self.ShipFrame == 6:
            self.ShipFrame = 1
        win.blit(BasicShipFrame[self.ShipFrame - 1], (self.xcor, self.ycor))

# Check if any options are clicked


def option_click_event(option, xmouse, ymouse):
    global running
    width_spacing = ((winWidth - option[3]) / 2)
    if width_spacing + option[3] > xmouse > width_spacing and option[4] + optionHeight > ymouse > option[4]:
        if option[0] == "quit":
            running = False
        print(option[0])

# This definition draws the options onto the pygame window


def create_options(option):
    global selectedOption
    global count
    mouse = pygame.mouse.get_pos()
    width_spacing = ((winWidth - option[3]) / 2)
    if selectedOption[0] == option[0]:
        win.blit(option[2], (width_spacing, option[4]))
    elif width_spacing + option[3] > mouse[0] > width_spacing and option[4] + optionHeight > mouse[1] > option[4]:
        win.blit(option[2], (width_spacing, option[4]))
        selectedOption = option
        player.ycor = option[4]
        player.xcor = width_spacing - 77
        optionArrayIndex = 0
        for u in optionTuple:
            if selectedOption[0] == u[0]:
                count = optionArrayIndex
            else:
                optionArrayIndex += 1
    else:
        win.blit(option[1], (width_spacing, option[4]))

# Cycles through the frames for the star images


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

# This definition handles if a keyboard press happens. Currently It detects if down button is pressed, up button and
# enter button.


def handlekeypress():
    global selectedOption
    global count
    global running
    if keys[pygame.K_DOWN]:
        count += 1
        for p in commandOptionArray:
            if player.ycor > 501:
                print(player.ycor)
                count = 0
                player.ycor = 276
            if selectedOption[0] == p:
                selectedOption = optionTuple[count]
                player.ycor += heightSpacing
                break
    if keys[pygame.K_UP]:
        count -= 1
        for p in commandOptionArray:
            if player.ycor < 400:
                print(player.ycor)
                count = len(optionTuple) - 1
                player.ycor = 651
            if selectedOption[0] == p:
                selectedOption = optionTuple[count]
                player.ycor -= heightSpacing
                break
    width_spacing = ((winWidth - selectedOption[3]) / 2)
    player.xcor = width_spacing - 77


    if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
        if selectedOption[0] == "quit":
            running = False
        else:
            print(selectedOption[0])

# This defnition draws the background, player and also updates pygame screen show everything displays onto the window


def drawgamewindow():
    # Displays Menu
    win.blit(bg, (0, 0))
    make_background()
    player.draw(win)
    for j in optionTuple:
        create_options(j)
    pygame.display.update()

# Set Running to true so the game loops forever


running = True
# creates the player object
player = PlayerShip(100, 351, 64, 64)
# The main loop where all the definitions are called and where everything is linked together
while running:
    clock.tick(12)                  # Controls frame rate
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()  # used to check what key on keyboard is pressed
        if event.type == pygame.QUIT:  # pygame.QUIT is the even in which the x button on window is pressed
            running = False            # set running to false so we break out of loop

        if event.type == pygame.MOUSEBUTTONUP:  # Checks if mouse is clicked
            mouse1 = pygame.mouse.get_pos()
            for x in optionTuple:
                option_click_event(x, mouse1[0], mouse1[1])
            print(mouse1)
        # Checks for key presses
        if event.type == pygame.KEYDOWN:
            handlekeypress()
        # checking for when the keys are pressed. Using event type so that keys wont register multiple times

    drawgamewindow()
pygame.quit()                           # quit pygame once using quits game

