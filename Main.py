import pygame  # importation for pygame

pygame.init()  # need to initialize pygame before using

clock = pygame.time.Clock()
winWidth = 700

widHeight = 750

optionHeight = 44

currentStarFrame = 0

currentStarFrame1 = 1

currentStarFrame2 = 2

win = pygame.display.set_mode((winWidth, widHeight))  # displays screen

#  option array (button name, image, highlighted image, image width, height spacing between each image)
#  If you want to add one more option, add 75 to height spacing between each image

startOption = ("start", pygame.image.load('Options/Start_Game.png'), pygame.image.load('Options/Start_Game_Highlighted.png'), 346, 350)  # 346x44

shopOption = ("shop", pygame.image.load('Options/Shop.png'), pygame.image.load('Options/Shop_Highlighted.png'), 146, 425)  # 146x44

settingsOption = ("settings", pygame.image.load('Options/Settings.png'), pygame.image.load('Options/Settings_Highlighted.png'), 274, 500)  # 274x44

quitOption = ("quit", pygame.image.load('Options/Quit.png'), pygame.image.load('Options/Quit_Highlighted.png'), 126, 575)  # 126x44

selectedOption = startOption

optionArray = (startOption, shopOption, settingsOption, quitOption)

bg = pygame.image.load('Menu/Main_Menu.png')
#  bg = pygame.transform.scale(bg, (700, 800))  # can resize image through pygame if need be
pygame.display.set_caption('BEYOND INFINITY')  # used to display name of window at the top
# Frames for stars
Star1 = [pygame.image.load('Background/Animated_Star1/Star0.png'), pygame.image.load('Background/Animated_Star1/Star1.png'),
                   pygame.image.load('Background/Animated_Star1/Star2.png')]

Star2 = [pygame.image.load('Background/Animated_Star2/Star0.png'), pygame.image.load('Background/Animated_Star2/Star1.png'),
                   pygame.image.load('Background/Animated_Star2/Star2.png')]

Star3 = [pygame.image.load('Background/Animated_Star3/Star0.png'), pygame.image.load('Background/Animated_Star3/Star1.png'),
                   pygame.image.load('Background/Animated_Star3/Star2.png')]

# Definition to draw game window


def option_click_event(option, xmouse, ymouse):
    global running
    width_spacing = ((winWidth - option[3]) / 2)
    if width_spacing + option[3] > xmouse > width_spacing and option[4] + optionHeight > ymouse > option[4]:
        if option[0] == "quit":
            running = False
        print(option[0])


def create_options(option):
    global selectedOption
    mouse = pygame.mouse.get_pos()
    width_spacing = ((winWidth - option[3]) / 2)

    if selectedOption[0] == option[0]:
        win.blit(option[2], (width_spacing, option[4]))
    elif width_spacing + option[3] > mouse[0] > width_spacing and option[4] + optionHeight > mouse[1] > option[4]:
        win.blit(option[2], (width_spacing, option[4]))
        selectedOption = option
    else:
        win.blit(option[1], (width_spacing, option[4]))


def create_optionss():
    mouse = pygame.mouse.get_pos()
    if 177+346 > mouse[0] > 177 and 350+44 > mouse[1] > 350:
        win.blit(startOption[2], (177, 350))  # 346x44
    else:
        win.blit(startOption, (177, 350))  # 346x44
    if 277+146 > mouse[0] > 277 and 425+44 > mouse[1] > 425:
        win.blit(shopOption[2], (277, 425))  # 146x44
    else:
        win.blit(shopOption, (277, 425))  # 146x44
    if 213+274 > mouse[0] > 213 and 500+44 > mouse[1] > 500:
        win.blit(settingsOption[2], (213, 500))  # 274x44
    else:
        win.blit(settingsOption, (213, 500))  # 274x44
    if 287+126 > mouse[0] > 287 and 575+44 > mouse[1] > 575:
        win.blit(quitOption[2], (287, 575))  # 126x44
    else:
        win.blit(quitOption, (287, 575))  # 126x44


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


def drawgamewindow():
    # Displays Menu
    win.blit(bg, (0, 0))
    make_background()
    for j in optionArray:
        create_options(j)

    # keys = pygame.key.get_pressed()
    pygame.display.update()


running = True  # Set Running to true so the game loops forever
# Main while loop to run game

while running:
    clock.tick(12)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pygame.QUIT is the even in which the x button on window is pressed
            running = False            # set running to false so we break out of loop

        if event.type == pygame.MOUSEBUTTONUP:
            mouse1 = pygame.mouse.get_pos()
            for x in optionArray:
                option_click_event(x, mouse1[0], mouse1[1])

            print(mouse1)
    drawgamewindow()
pygame.quit()                           # quit pygame once using quits game

