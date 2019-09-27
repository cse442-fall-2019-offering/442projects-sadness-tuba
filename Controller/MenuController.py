import pygame  # importation for pygame

import Model
import time
from Model import optionTuple, backOption

from View.MainMenuView import drawMainWindow, drawBlankWindow, winWidth, optionHeight, FPS, background, player, transition, widHeight, \
    drawSettingsWindow

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()  # need to initialize pygame before using

running = True
currentPage = "main"


# Use for determining which option gets highlighted when uses keyboard pressed
commandOptionArray = []


# This definition handles if a keyboard press happens. Currently It detects if down button is pressed, up button and
# enter button.


def handleKeypress(keys):
    global running, currentPage
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
            transition(winWidth, widHeight)
            running = False
        elif Model.selectedOption.name == "settings":
            transition(winWidth, widHeight)
            currentPage = "settings"
        elif Model.selectedOption.name == "start":
            transition(winWidth, widHeight)
            currentPage = "game"
        print(Model.selectedOption.name)
        return Model.selectedOption.name


def option_click_event(option, xmouse, ymouse):
    global running, currentPage
    width_spacing = ((winWidth - option.imgWidth) / 2)
    if width_spacing + option.imgWidth > xmouse > width_spacing and option.yAxisImageSpacing + optionHeight > ymouse > option.yAxisImageSpacing:
        transition(winWidth, widHeight)
        if option.name == "quit":
            running = False
        elif option.name == "settings":
            currentPage = "settings"
        elif option.name == "start":
            currentPage = "game"
        print(option.name)
        return option.name
    elif option.name == "back" and 25 + option.imgWidth > xmouse > 25 and option.yAxisImageSpacing + optionHeight > ymouse > option.yAxisImageSpacing:
        transition(winWidth, widHeight)
        currentPage = "main"
        print(option.name)
        return option.name

def main():
    global running, currentPage
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
        if currentPage == "main":
            drawMainWindow(mouse, dt, menuBackground, player)
        elif currentPage == "settings":
            drawSettingsWindow(mouse)
        elif currentPage == "game":
            drawBlankWindow(mouse)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()  # used to check what key on keyboard is pressed
            if event.type == pygame.QUIT:  # pygame.QUIT is the even in which the x button on window is pressed
                running = False  # set running to false so we break out of loop
            if event.type == pygame.MOUSEBUTTONUP:  # Checks if mouse is clicked
                print(mouse)
                if currentPage == "main":
                    for x in optionTuple:
                        option_click_event(x, mouse[0], mouse[1])
                else:
                    option_click_event(backOption, mouse[0], mouse[1])
            if event.type == pygame.KEYDOWN:
                if currentPage == "main":
                    handleKeypress(keys)
                if event.key == pygame.K_ESCAPE and currentPage != "main":
                    currentPage = "main"
                    transition(winWidth, widHeight)
            # checking for when the keys are pressed. Using event type so that keys wont register multiple times

    pygame.quit()


if __name__ == "__main__":
    main()
