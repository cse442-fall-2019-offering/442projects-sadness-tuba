# importation for pygame and os
import random
import pygame
from View.ParentView import View


# Class for defining the gameplay portion
class GameplayView(View):
    def __init__(self):
        super(GameplayView, self).__init__()
        self.name = "Gameplay"
        self.bg = pygame.image.load('Menu/Blank_Page.png')
        # creates player class
        self.player = Player(310, 600, 64, 64, 'PlayerShips/Infinity', 0, 'single_middle')
        # List of each bullet
        self.bulletArray = pygame.sprite.Group()
        self.bulletTimer = 0
        # Sections
        self.section1 = Section(1, 0, 180, -96, 10, 20, 1)
        self.section2 = Section(2, 244, 392, -96, 10, 20, 5)
        self.section3 = Section(3, 456, 636, -96, 10, 20, 1)
        self.sectionArray = [self.section1, self.section2, self.section3]
        # Enemy Formation
        self.formationTypes = ['imp_v1', 'impaler_diagonal1', 'impaler_diagonal2', 'imperier_v1', 'imperier_^1']
        self.enemyList = pygame.sprite.Group()

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
        self.enemy_hit()
        self.player.update(self.screen, dt)
        pygame.display.update()

    def key_event(self, key):
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            if self.player.ycor + self.player.playerSpeed < self.windowHeight - 70:
                self.player.ycor += self.player.playerSpeed
        if key[pygame.K_UP] or key[pygame.K_w]:
            if self.player.ycor - self.player.playerSpeed > 0:
                self.player.ycor -= self.player.playerSpeed
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            if self.player.xcor + self.player.playerSpeed > 0:
                self.player.xcor -= self.player.playerSpeed
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            if self.player.xcor + self.player.playerSpeed < self.windowWidth - 60:
                self.player.xcor += self.player.playerSpeed
        if key[pygame.K_SPACE]:
            if self.bulletTimer <= 0:
                self.bulletTimer = self.player.fireRate
                self.shoot_bullet()

    def shoot_bullet(self):
        # player shoots bullet. shootType can be customized to change the starting position of the bullet and how many bullets shot
        if self.player.shootType == 'single_middle':
            bullet = Bullet(self.player.xcor + (self.player.rect.width / 2 - 5), self.player.ycor, self.player.currentBullet[1], self.player.currentBullet[2], self.player.currentBullet[3], 0, self.player)
            self.bulletArray.add(bullet)
            bullet.sound.play()

    def spawn_enemies(self, section, dt):
        # spawns enemy formation in the section. enemyFormation is chosen randomly. Adds enemies from the enemyFormation to enemyList
        section.CD -= dt
        if section.CD <= 0:
            section.CD = random.uniform(section.earliestCD, section.latestCD)
            enemyFormation = EnemyFormation(random.choice(self.formationTypes), section)
            for i in enemyFormation.enemyGroup:
                self.enemyList.add(i)

    def move_enemies(self, dt):
        # moves all enemies on the screen and removes them when they leave the screen
        for i in self.enemyList:
            i.move()
            i.update(self.screen, dt)
            # Debug hitbox. Shows enemy hitboxes in red rectangle.
            # pygame.draw.rect(self.screen, (255, 0, 0), i.hitbox, 3)
            if i.ycor > self.windowHeight + 96:
                self.enemyList.remove(i)

    def move_bullets(self, dt):
        # moves all player bullets on the screen and removes them when they leave the screen
        for bullet in self.bulletArray:
            bullet.move()
            bullet.update(self.screen, dt)
            if bullet.ycor < -20:
                self.bulletArray.remove(bullet)

    def enemy_hit(self):
        for i in self.enemyList:
            for bullet in self.bulletArray:
                if bullet.xcor > i.hitbox[0] and bullet.xcor < i.hitbox[0] + i.hitboxX:
                    if bullet.ycor > i.hitbox[1] and bullet.ycor < i.hitbox[1] + i.hitboxY:
                        self.bulletArray.remove(bullet)
                        self.enemyList.remove(i)

class GameSprite(pygame.sprite.Sprite):
    # class for a Sprite. To create a sprite you must provide: (x coordinate, y coordinate, size of the image, array of
    # all the images, and the starting frame)
    def __init__(self, xcor, ycor, width, height, images, starting_frame):
        super(GameSprite, self).__init__()
        self.xcor = xcor
        self.ycor = ycor
        # creates rectangle for the sprite
        self.rect = pygame.Rect((xcor, ycor), (width, height))
        self.images = View.load_images(images)
        # time it takes for the the sprite moves to the next frame
        self.animationTime = .08
        self.currentTime = 0
        self.index = starting_frame

    def update_time_dependent(self, screen, dt):
        # Updates the image of Sprite based on animation_time. Must provide: (the window, milliseconds since last frame)
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.index = (self.index + 1) % len(self.images)
        screen.blit(self.images[self.index], (self.xcor, self.ycor))

    def update(self, screen, dt):
        # This is the method that's being called when 'all_sprites.update(dt)' is called. Must provide:
        # (the window, milliseconds since last frame)
        self.update_time_dependent(screen, dt)


class Player(GameSprite):
    # player class (xcor, ycor, width, height, folder containing the images, starting frame, player's shooting type)
    def __init__(self, xcor, ycor, width, height, images, starting_frame, shoot_type):
        super().__init__(xcor, ycor, width, height, images, starting_frame)
        self.shootType = shoot_type
        self.fireRate = .3
        self.playerSpeed = 7
        self.bulletSpeed = 10
        self.smallBasicBullet = ['sm_basic_bullet', 10, 24, 'Projectiles/Small_Basic_Bullet',
                                 pygame.mixer.Sound('Projectiles/Basic_Bullet.wav')]
        self.currentBullet = self.smallBasicBullet


class Bullet(GameSprite):
    # bullet class (xcor, ycor, width, height, folder containing the images, starting frame, player)
    def __init__(self, xcor, ycor, width, height, images, starting_frame, player):
        super().__init__(xcor, ycor, width, height, images, starting_frame)
        self.player = player
        self.name = player.currentBullet[0]
        self.sound = player.currentBullet[4]

    def move(self):
        # moves the bullet. can customize bullet pathing
        if self.name == 'sm_basic_bullet':
            self.ycor -= self.player.bulletSpeed


class Enemy(GameSprite):
    # enemy class (xcor, ycor, width, height, folder containing the images, starting frame, name of enemy, health, speed)
    def __init__(self, xcor, ycor, width, height, images, starting_frame, name, health, speed, hitboxX, hitboxY):
        super().__init__(xcor, ycor, width, height, images, starting_frame)
        self.name = name
        self.speed = speed
        self.health = health
        self.hitboxX = hitboxX
        self.hitboxY = hitboxY
        self.hitbox = (self.xcor + 10, self.ycor + 10, hitboxX, hitboxY)

    def move(self):
        # moves the enemy. can customize enemy pathing
        if self.name == 'Impaler' or 'Imperier':
            self.ycor += self.speed
            self.hitbox = (self.xcor + 10, self.ycor + 10, self.hitboxX, self.hitboxY)


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
            enemyShip = Enemy(xcor, ycor, 96, 96, 'EnemyShips/Lvl1_Enemy_Impaler', 0, enemy, 3, 1, 75, 75)
        elif enemy == 'Imperier':
            enemyShip = Enemy(xcor, ycor, 64, 64, 'EnemyShips/Lvl1_Enemy_Imperier', 0, enemy, 2, 1, 45, 50)
        enemyShip.xcor = xcor
        enemyShip.ycor = ycor
        return enemyShip
