# importation for pygame, os and all the views
import pygame
import os
import View.MainMenuView, View.QuitView, View.SettingsView, View.GameplayView, View.ParentView


def main():
    os.chdir("..")
    pygame.mixer.pre_init(44100, -16, 1, 512)
    # need to initialize pygame before using
    pygame.init()
    # setting the volume
    pygame.mixer.music.set_volume(View.ParentView.View().soundEffectVolume)
    # cv is current view
    cv = View.MainMenuView.MainMenuView()
    # clock that the game is running on
    clock = pygame.time.Clock()
    # plays menu music
    cv.play_music('Sprites/Menu/Menu_Track.wav')
    # while the current view is running, loop
    while cv.is_running():
        dt = clock.tick(60) / 1000
        mouse = pygame.mouse.get_pos()
        # draws screen
        cv.draw(mouse, dt)
        # listens for event
        for event in pygame.event.get():
            # pygame.QUIT is the even in which the x button on window is pressed
            if event.type == pygame.QUIT:
                cv = View.QuitView.QuitView()
            if cv.name != "Gameplay":
                if event.type == pygame.MOUSEBUTTONUP:
                    print(mouse)
                    cv = cv.click_event(mouse)
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    cv = cv.key_event(key)
        if cv.name == "Gameplay":
            keys = pygame.key.get_pressed()  # checking pressed keys
            cv.key_event(keys)


if __name__ == "__main__":
    main()
