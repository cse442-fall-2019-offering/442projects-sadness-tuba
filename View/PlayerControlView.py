# importation for pygame, MainMenuView and View and Sprite class
import pygame
import View.ShipSelectView as shipselect
import View.GameplayView as gameplay
from View.ParentView import View, Sprite

# Ship select view controls ship select menu


class PlayerControlView(View):
    # ShipSelectView, child class of ParentView
    def __init__(self):
        super(PlayerControlView, self).__init__()
        self.name = "PlayerControls"
        self.bg = pygame.image.load('Sprites/Menu/Player_Controls_Page.png')

    def draw(self, mouse, dt):
        # repeatedly draws the screen, must provide: (mouse position, milliseconds since last frame)
        self.screen.blit(self.bg, (0, 0))
        # pygame.draw.rect(self.screen, (255, 255, 255),
        # (self.baseShip.xcor - 20, self.baseShip.ycor - 15, 100, 100), 2)
        pygame.display.update()

    def key_event(self, key):
        # returns to MainMenuView after user pushes escape. Otherwise returns self. Must provide: (key pressed)
        if key[pygame.K_ESCAPE]:
            self.transition()
            return shipselect.ShipSelectView()
        if key[pygame.K_KP_ENTER] or key[pygame.K_RETURN]:
            self.transition()
            return gameplay.GameplayView()
        else:
            return self

    def click_event(self, mouse):
        return self




