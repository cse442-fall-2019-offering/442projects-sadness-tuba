import pygame  # importation for pygame
import os
import View.MainMenuView, View.QuitView, View.SettingsView


def main():
    os.chdir("..")
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()  # need to initialize pygame before using
    pygame.mixer.music.set_volume(View.SettingsView.SettingsView().soundEffectVolume)  # setting the volume
    cv = View.MainMenuView.MainMenuView()  # cv is current view
    clock = pygame.time.Clock()
    while cv.isRunning():
        dt = clock.tick(60) / 1000
        mouse = pygame.mouse.get_pos()
        cv.draw(mouse, dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT is the even in which the x button on window is pressed
                cv = View.QuitView.QuitView()
            if event.type == pygame.MOUSEBUTTONUP:
                cv = cv.click_event(mouse)
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                cv = cv.key_event(key)


if __name__ == "__main__":
    main()
