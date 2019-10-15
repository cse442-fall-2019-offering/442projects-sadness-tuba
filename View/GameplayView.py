import pygame  # importation for pygame
import View.MainMenuView as main

from View.ParentView import View, PlayerShip

# CLass for defining the gameplay portion


class GameplayView(View):
    def __init__(self):
        super(GameplayView, self).__init__()
        self.name = "Gameplay"
        self.bg = pygame.image.load('Menu/Blank_Page.png')
        self.basicPlayerShip = PlayerShip(310, 600, 64, self.BasicShipFrames, 0)
    # Draws background and Player ship

    def draw(self, mouse, dt):
        # repeatedly draws the screen, must provide: (mouse position, milliseconds since last frame)
        self.screen.blit(self.bg, (0, 0))
        self.basicPlayerShip.update(self.screen, dt)
        pygame.display.update()
    # Moves play up when user presses "w"

    def move_player_up(self):
        if self.basicPlayerShip.ycor - self.basicPlayerShip.yspeed > 0:
            self.basicPlayerShip.ycor -= self.basicPlayerShip.yspeed
    # 680
    # Moves play up when user presses "s"

    def move_player_down(self):
        if self.basicPlayerShip.ycor + self.basicPlayerShip.yspeed < self.windowHeight - 70:
            self.basicPlayerShip.ycor += self.basicPlayerShip.yspeed
    # 640
    # Moves play up when user presses "d"

    def move_player_right(self):
        if self.basicPlayerShip.xcor + self.basicPlayerShip.xspeed < self.windowWidth - 60:
            self.basicPlayerShip.xcor += self.basicPlayerShip.xspeed

    # Moves play up when user presses "a"
    def move_player_left(self):
        if self.basicPlayerShip.xcor + self.basicPlayerShip.xspeed > 0:
            self.basicPlayerShip.xcor -= self.basicPlayerShip.xspeed
