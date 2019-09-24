import pygame  # importation for pygame

import Model
import time
from Model import optionTuple

from View.MainMenuView import drawGameWindow, winWidth, optionHeight, FPS, background, player, transition, widHeight, \
    drawNextWindow

pygame.init()  # need to initialize pygame before using

running = True
shopRun = False
startStageRun = False
settingRun = False



# Use for determining which option gets highlighted when uses keyboard pressed
commandOptionArray = []


# This definition handles if a keyboard press happens. Currently It detects if down button is pressed, up button and
# enter button.


def handleKeypress(keys):
    global running
    global shopRun
    global startStageRun
    global settingRun
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
        if Model.selectedOption.name == "start":
            transition(winWidth, widHeight)
            startStageRun = True
            while (startStageRun):
                drawNextWindow()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            startStageRun = False
        if Model.selectedOption.name == "shop":
            transition(winWidth, widHeight)
            shopRun = True
            while (shopRun):
                drawNextWindow()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            shopRun = False
        if Model.selectedOption.name == "settings":
            transition(winWidth, widHeight)
            settingRun = True
            while (settingRun):
                drawNextWindow()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            settingRun = False
        else:
            print(Model.selectedOption.name)


def option_click_event(option, xmouse, ymouse):
    global running
    global shopRun
    global startStageRun
    global settingRun
    width_spacing = ((winWidth - option.imgWidth) / 2)
    if width_spacing + option.imgWidth > xmouse > width_spacing and option.yAxisImageSpacing + optionHeight > ymouse > option.yAxisImageSpacing:
        if option.name == "quit":
            transition(winWidth, widHeight)
            running = False
        if option.name == "start":
            transition(winWidth, widHeight)
            startStageRun = True
            while (startStageRun):
                drawNextWindow()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            startStageRun = False
        if option.name == "shop":
            transition(winWidth, widHeight)
            shopRun = True
            while (shopRun):
                drawNextWindow()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            shopRun = False
        if option.name == "settings":
            transition(winWidth, widHeight)
            settingRun = True
            while (settingRun):
                drawNextWindow()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            settingRun = False
        print(option.name)
        return option.name


def main():
    global running
    # Starting height for first option
    menuBackground = pygame.sprite.Group()
    clock = pygame.time.Clock()
    for z in optionTuple:
        commandOptionArray.append(z.name)
    # puts all background images inside Sprite.Group
    for b in background:
        menuBackground.add(b)
    while running:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.
        mouse = pygame.mouse.get_pos()
        # Controls frame rate
        drawGameWindow(mouse, dt, menuBackground, player)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()  # used to check what key on keyboard is pressed
            if event.type == pygame.QUIT:  # pygame.QUIT is the even in which the x button on window is pressed
                running = False  # set running to false so we break out of loop
            if event.type == pygame.MOUSEBUTTONUP:  # Checks if mouse is clicked
                print(mouse)
                for x in optionTuple:
                    option_click_event(x, mouse[0], mouse[1])
            # Checks for key presses
            if event.type == pygame.KEYDOWN:
                handleKeypress(keys)
            # checking for when the keys are pressed. Using event type so that keys wont register multiple times

    pygame.quit()


if __name__ == "__main__":
    main()
