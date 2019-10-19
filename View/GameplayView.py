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
        self.player = Player(GameSprite(310, 600, 64, 64, 'PlayerShips/Infinity', 0), 'single_middle')
        # List of each bullet
        self.bulletArray = []
        self.bulletTimer = 0
        # Sections
        self.section1 = Section(1, 0, 180, -96, 10, 20, 1)
        self.section2 = Section(2, 244, 392, -96, 10, 20, 5)
        self.section3 = Section(3, 456, 636, -96, 10, 20, 1)
        self.sectionArray = [self.section1, self.section2, self.section3]
        # Enemy Formation
        self.formationTypes = ['imp_v1', 'impaler_diagonal1', 'impaler_diagonal2', 'imperier_v1', 'imperier_^1']
        self.formationArray = []
        self.enemyArray = []
        # self.vFormation1 = EnemyFormation('imp_v1', self.section1)

    # Draws background and Player ship

    def draw(self, mouse, dt):
        # decreases bullet timer to manage fire rate
        self.bulletTimer -= dt
        # repeatedly draws the screen, must provide: (mouse position, milliseconds since last frame)
        self.screen.blit(self.bg, (0, 0))
        for i in self.sectionArray:
            self.spawn_enemies(i, dt)
        self.move_enemies(dt)
        self.move_bullets(dt)
        self.player.gameSprite.update(self.screen, dt)
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

    def shoot_bullet(self):
        # player shoots bullet. shootType can be customized to change the starting position of the bullet and how many bullets shot
        if self.player.shootType == 'single_middle':
            bullet = Bullet(self.player, self.player.gameSprite.xcor + (self.player.gameSprite.rect.width / 2 - 5))
            self.bulletArray.append(bullet)
            bullet.sound.play()

    def spawn_enemies(self, section, dt):
        # spawns enemy formation in the section. enemyFormation is chosen randomly. Adds enemies from the enemyFormation to enemyArray
        section.CD -= dt
        if section.CD <= 0:
            section.CD = random.uniform(section.earliestCD, section.latestCD)
            enemyFormation = EnemyFormation(random.choice(self.formationTypes), section)
            for i in enemyFormation.enemyGroup:
                self.enemyArray.append(i)

    def move_enemies(self, dt):
        # moves all enemies on the screen and removes them when they leave the screen
        for i in self.enemyArray:
            i.move()
            i.gameSprite.update(self.screen, dt)
            if i.gameSprite.ycor > self.windowHeight + 96:
                self.enemyArray.remove(i)

    def move_bullets(self, dt):
        # moves all player bullets on the screen and removes them when they leave the screen
        for bullet in self.bulletArray:
            bullet.move()
            bullet.gameSprite.update(self.screen, dt)
            if bullet.gameSprite.ycor < -20:
                self.bulletArray.remove(bullet)


class Player(object):
    # player class (GameSprite)
    def __init__(self, game_sprite, shoot_type):
        self.gameSprite = game_sprite
        self.shootType = shoot_type
        self.fireRate = .5
        self.playerSpeed = 4
        self.bulletSpeed = 5
        self.smallBasicBullet = ['sm_basic_bullet', 10, 24, 'Projectiles/Small_Basic_Bullet',
                                 pygame.mixer.Sound('Projectiles/Basic_Bullet.wav')]
        self.currentBullet = self.smallBasicBullet


class Bullet(object):
    # bullet class (xcoordinate, ycoordinate, image width, image height, bullet png, bullet wav)
    def __init__(self, player, xaxis):
        self.player = player
        self.name = player.currentBullet[0]
        self.sound = player.currentBullet[4]
        self.gameSprite = GameSprite(xaxis, player.gameSprite.ycor, player.currentBullet[1], player.currentBullet[2],
                                     player.currentBullet[3], 0)

    def move(self):
        # moves the bullet. can customize bullet pathing
        if self.name == 'sm_basic_bullet':
            self.gameSprite.ycor -= self.player.bulletSpeed


class Enemy(object):
    # enemy class (name, GameSprite, health, speed)
    def __init__(self, name, game_sprite, health, speed):
        self.name = name
        self.gameSprite = game_sprite
        self.speed = speed
        self.health = health

    def move(self):
        # moves the enemy. can customize enemy pathing
        if self.name == 'Impaler' or 'Imperier':
            self.gameSprite.ycor += self.speed


class Section(object):
    # section enemies spawn class (section number, starting x axis, ending x axis, y axis that enemies spawn,
    # earliest time enemy can spawn, latest enemy can spawn)
    def __init__(self, section, start_point, end_point, yaxis, earliestCD, latestCD, CD):
        self.section = section
        self.startPoint = start_point
        self.endPoint = end_point
        self.midPoint = (end_point + start_point) / 2
        self.xaxis = (start_point, end_point)
        self.yaxis = yaxis
        self.earliestCD = earliestCD
        self.latestCD = latestCD
        self.CD = CD


class EnemyFormation(object):
    # enemy formation class (string formation_type, class Section)
    def __init__(self, formation_type, section):
        self.formationType = formation_type
        self.section = section
        self.enemyGroup = []
        # Enemies
        # ['Impaler', GameSprite(section.startPoint, section.yaxis, 96, 96, 'EnemyShips/Lvl1_Enemy_Impaler', 0), 3, 1]
        # ['Imperier', GameSprite(section.startPoint, section.yaxis, 64, 64, 'EnemyShips/Lvl1_Enemy_Imperier', 0), 2, 1]

        if formation_type == 'imp_v1':
            self.enemyGroup.append(self.create_enemy('Impaler', section.midPoint - 16, section.yaxis))
            self.enemyGroup.append(self.create_enemy('Imperier', section.startPoint, section.yaxis - 64))
            self.enemyGroup.append(self.create_enemy('Imperier', section.endPoint, section.yaxis - 64))
        elif formation_type == 'impaler_diagonal1':
            self.enemyGroup.append(self.create_enemy('Impaler', section.startPoint, section.yaxis))
            self.enemyGroup.append(self.create_enemy('Impaler', section.endPoint - 32, section.yaxis - 64))
        elif formation_type == 'impaler_diagonal2':
            self.enemyGroup.append(self.create_enemy('Impaler', section.startPoint, section.yaxis - 64))
            self.enemyGroup.append(self.create_enemy('Impaler', section.endPoint - 32, section.yaxis))
        elif formation_type == 'imperier_v1':
            self.enemyGroup.append(self.create_enemy('Imperier', section.midPoint, section.yaxis))
            self.enemyGroup.append(self.create_enemy('Imperier', section.startPoint + 16, section.yaxis - 64))
            self.enemyGroup.append(self.create_enemy('Imperier', section.endPoint - 16, section.yaxis - 64))
        elif formation_type == 'imperier_^1':
            self.enemyGroup.append(self.create_enemy('Imperier', section.midPoint, section.yaxis - 64))
            self.enemyGroup.append(self.create_enemy('Imperier', section.startPoint + 16, section.yaxis))
            self.enemyGroup.append(self.create_enemy('Imperier', section.endPoint - 16, section.yaxis))

    def create_enemy(self, enemy, xcor, ycor):
        if enemy == 'Impaler':
            enemyShip = Enemy('Impaler', GameSprite(xcor, ycor, 96, 96,'EnemyShips/Lvl1_Enemy_Impaler', 0), 3, 1)
        elif enemy == 'Imperier':
            enemyShip = Enemy('Imperier', GameSprite(xcor, ycor, 64, 64, 'EnemyShips/Lvl1_Enemy_Imperier', 0), 2, 1)
        enemyShip.gameSprite.xcor = xcor
        enemyShip.gameSprite.ycor = ycor
        return enemyShip
