# importation for pygame and os
import random
import pygame
from View.ParentView import View, GameSprite

# CLass for defining the gameplay portion
class GameplayView(View):
    def __init__(self):
        super(GameplayView, self).__init__()
        self.name = "Gameplay"
        self.bg = pygame.image.load('Menu/Blank_Page.png')

        self.shipSpeed = 4
        self.fireRate = .5
        self.bulletTimer = 0
        self.player = GameSprite(310, 600, 64, 64, self.BasicShipFrames, 0, self.shipSpeed)

        self.bulletSpeed = 5
        self.currentBullet = [pygame.image.load('Projectiles/Small_Basic_Bullet.png')]
        self.bulletSound = pygame.mixer.Sound('Projectiles/Basic_Bullet.wav')
        # List of each bullet
        self.bullet_list = pygame.sprite.Group()

        self.EnemyImpalerLvl1 = GameSprite(random.randint(0, 500), -96, 96, 96, self.EnemyImpalerShipLvl1Frames, 0, 3)
    # Draws background and Player ship

    def draw(self, mouse, dt):
        # decreases bullet timer to manage fire rate
        self.bulletTimer -= dt
        # repeatedly draws the screen, must provide: (mouse position, milliseconds since last frame)
        self.screen.blit(self.bg, (0, 0))
        self.player.update(self.screen, dt)
        for bullet in self.bullet_list:
            bullet.ycor -= bullet.yspeed
            if bullet.ycor < -10:
                self.bullet_list.remove(bullet)
        self.bullet_list.update(self.screen, dt)
        self.move_enemy_ship_down(self.EnemyImpalerLvl1)
        self.EnemyImpalerLvl1.update(self.screen, dt)
        pygame.display.update()

    def key_event(self, key):
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            if self.player.ycor + self.player.yspeed < self.windowHeight - 70:
                self.player.ycor += self.player.yspeed
        if key[pygame.K_UP] or key[pygame.K_w]:
            if self.player.ycor - self.player.yspeed > 0:
                self.player.ycor -= self.player.yspeed
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            if self.player.xcor + self.player.xspeed > 0:
                self.player.xcor -= self.player.xspeed
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            if self.player.xcor + self.player.xspeed < self.windowWidth - 60:
                self.player.xcor += self.player.xspeed
        if key[pygame.K_SPACE]:
            if self.bulletTimer <= 0:
                self.bulletTimer = self.fireRate
                self.bulletSound.play()
                self.bullet_list.add(GameSprite(self.player.xcor + (self.player.rect.width/2 - 5), self.player.ycor, 10, 24, self.currentBullet, 0, self.bulletSpeed))

    def move_enemy_ship_down(self, enemyShip):
        enemyShip.ycor += enemyShip.yspeed
