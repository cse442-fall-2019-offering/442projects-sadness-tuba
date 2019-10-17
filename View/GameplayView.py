# importation for pygame and os
import random
import pygame
from View.ParentView import View, GameSprite


# Class for defining the gameplay portion
class GameplayView(View):
    def __init__(self):
        super(GameplayView, self).__init__()
        self.name = "Gameplay"
        self.bg = pygame.image.load('Menu/Blank_Page.png')
        # creates player class
        self.player = Player(GameSprite(310, 600, 64, 64, self.BasicShipFrames, 0))

        self.bulletTimer = 0
        # List of each bullet
        self.bulletList = pygame.sprite.Group()

        self.EnemyImpalerLvl1 = Enemy(GameSprite(random.randint(0, 500), -96, 96, 96, self.EnemyImpalerShipLvl1Frames, 0))
    # Draws background and Player ship

    def draw(self, mouse, dt):
        # decreases bullet timer to manage fire rate
        self.bulletTimer -= dt
        # repeatedly draws the screen, must provide: (mouse position, milliseconds since last frame)
        self.screen.blit(self.bg, (0, 0))
        self.move_enemy_ship_down(self.EnemyImpalerLvl1)
        self.player.gameSprite.update(self.screen, dt)
        for bullet in self.bulletList:
            bullet.ycor -= self.player.bulletSpeed
            if bullet.ycor < -10:
                self.bulletList.remove(bullet)
        self.EnemyImpalerLvl1.gameSprite.update(self.screen, dt)
        self.bulletList.update(self.screen, dt)
        pygame.display.update()

    def key_event(self, key):
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            if self.player.gameSprite.ycor + self.player.playerSpeed < self.windowHeight - 70:
                self.player.gameSprite.ycor += self.player.playerSpeed
        if key[pygame.K_UP] or key[pygame.K_w]:
            if self.player.gameSprite.ycor - self.player.playerSpeed > 0:
                self.player.gameSprite.ycor -= self.player.playerSpeed
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            if self.player.gameSprite.xcor + self.player.playerSpeed > 0:
                self.player.gameSprite.xcor -= self.player.playerSpeed
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            if self.player.gameSprite.xcor + self.player.playerSpeed < self.windowWidth - 60:
                self.player.gameSprite.xcor += self.player.playerSpeed
        if key[pygame.K_SPACE]:
            if self.bulletTimer <= 0:
                self.bulletTimer = self.player.fireRate
                self.shoot_bullet()

    def move_enemy_ship_down(self, enemyShip):
        enemyShip.gameSprite.ycor += enemyShip.speed

    def shoot_bullet(self):
        bullet = Bullet(self.player.gameSprite.xcor + (self.player.gameSprite.rect.width / 2 - 5), self.player.gameSprite.ycor, self.player.currentBullet[2], self.player.currentBullet[3], self.player.currentBullet[4], self.player.currentBullet[5])
        self.bulletList.add(bullet.gameSprite)
        bullet.sound.play()


class Player(object):
    # player class (GameSprite)
    def __init__(self, game_sprite):
        self.gameSprite = game_sprite
        self.fireRate = .5
        self.playerSpeed = 4
        self.bulletSpeed = 5
        self.smallBasicBullet = [game_sprite.xcor + (game_sprite.rect.width / 2 - 5), game_sprite.ycor, 10, 24, [pygame.image.load('Projectiles/Small_Basic_Bullet.png')], pygame.mixer.Sound('Projectiles/Basic_Bullet.wav')]
        self.currentBullet = self.smallBasicBullet


class Bullet(object):
    # bullet class (xcoordinate, ycoordinate, image width, image height, bullet png, bullet wav)
    def __init__(self, xcor, ycor, width, height, bullet_sprite, bullet_sound):
        self.sound = bullet_sound
        self.gameSprite = GameSprite(xcor, ycor, width, height, bullet_sprite, 0)


class Enemy(object):
    # player class (GameSprite)
    def __init__(self, game_sprite):
        self.gameSprite = game_sprite
        self.speed = 1


