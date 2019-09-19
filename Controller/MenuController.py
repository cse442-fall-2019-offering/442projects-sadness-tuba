import pygame  # importation for pygame

import Model

from Model import optionTuple

from View.MainMenuView import player, drawgamewindow, winWidth, optionHeight

pygame.init()  # need to initialize pygame before using

clock = pygame.time.Clock()

running = True

spacing_from_option = 77

# Starting height for first option
startingHeight = 350

# Use for determining which option gets highlighted when uses keyboard pressed
commandOptionArray = []
for z in optionTuple:
    z.yAxisImageSpacing = startingHeight
    startingHeight += 75
    commandOptionArray.append(z.name)

# This definition handles if a keyboard press happens. Currently It detects if down button is pressed, up button and
# enter button.


def handlekeypress():
    global running
    if keys[pygame.K_DOWN]:
        for p in commandOptionArray:
            if Model.selectedOption.name == p:
                for idx, item in enumerate(optionTuple):
                    if Model.selectedOption == item and idx < len(optionTuple) - 1:
                        Model.selectedOption = optionTuple[idx + 1]
                        break
                    elif Model.selectedOption == item and idx + 1 > len(optionTuple) - 1:
                        Model.selectedOption = optionTuple[0]
                        break
                player.ycor = Model.selectedOption.yAxisImageSpacing
                break
    if keys[pygame.K_UP]:
        for p in commandOptionArray:
            if Model.selectedOption.name == p:
                for idx, item in enumerate(optionTuple):
                    if Model.selectedOption == item and idx != 0:
                        Model.selectedOption = optionTuple[idx - 1]
                        break
                    elif Model.selectedOption == item and idx == 0:
                        Model.selectedOption = optionTuple[len(optionTuple) - 1]
                        break
                player.ycor = Model.selectedOption.yAxisImageSpacing
                break
    width_spacing = ((winWidth - Model.selectedOption.imgWidth) / 2)
    player.xcor = width_spacing - 77

    if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
        if Model.selectedOption.name == "quit":
            running = False
        else:
            print(Model.selectedOption.name)

def option_click_event(option, xmouse, ymouse):
    global running
    width_spacing = ((winWidth - option.imgWidth) / 2)
    if width_spacing + option.imgWidth > xmouse > width_spacing and option.yAxisImageSpacing + optionHeight > ymouse > option.yAxisImageSpacing:
        if option.name == "quit":
            running = False
        print(option.name)

while running:
    clock.tick(12)
    mouse = pygame.mouse.get_pos()
    # Controls frame rate
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()  # used to check what key on keyboard is pressed
        if event.type == pygame.QUIT:  # pygame.QUIT is the even in which the x button on window is pressed
            running = False            # set running to false so we break out of loop

        if event.type == pygame.MOUSEBUTTONUP:  # Checks if mouse is clicked
            for x in optionTuple:
                option_click_event(x, mouse[0], mouse[1])
        # Checks for key presses
        if event.type == pygame.KEYDOWN:
            handlekeypress()
        # checking for when the keys are pressed. Using event type so that keys wont register multiple times

    drawgamewindow(mouse)
pygame.quit()