# importation for pygame and os
import copy
import random
import pygame
import math
from View.ParentView import View

globalPlayerScore = 0

# Class for defining the gameplay portion
class GameplayView(View):
    def __init__(self):
        super(GameplayView, self).__init__()
        self.name = "Gameplay"
        self.bg = pygame.image.load('Sprites/Menu/Blank_Page.png')
        # creates player class
        self.player = Player(310, 600, 64, 64, 'Sprites/PlayerShips/Infinity/Infinity_Flying', 0, 'single_middle', 'Infinity', 'Sprites/PlayerShips/Infinity/Infinity_Destroyed')
        # List of each bullet
        self.bulletArray = pygame.sprite.Group()
        self.enemyBulletArray = pygame.sprite.Group()
        self.bulletTimer = 0
        self.explosionArray = pygame.sprite.Group()
        # Sections
        self.section1 = Section(1, 0, 180, -96, 10, 20, 1)
        self.section2 = Section(2, 244, 392, -96, 10, 20, 5)
        self.section3 = Section(3, 456, 636, -96, 10, 20, 1)
        self.sectionArray = [self.section1, self.section2, self.section3]
        # Enemy Formation ['imp_v1', 'impaler_diagonal1', 'impaler_diagonal2', 'imperier_v1', 'imperier_^1', 'scatter_v1']
        self.formationTypes = ['imp_v1', 'impaler_diagonal1', 'impaler_diagonal2', 'imperier_v1', 'imperier_^1', 'scatter_v1', 'scatter_^1', 'scatimp_^1']
        self.enemyList = pygame.sprite.Group()
        # Display
        self.heart = View.load_images('Sprites/Player_Info/Heart')
        self.allFonts = pygame.font.get_fonts()
        self.font = pygame.font.SysFont(self.allFonts[8], 24)

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
        self.player_hit(dt)
        self.player.update(self.screen, dt)
        for j in self.explosionArray:
            j.update(self.screen, dt)
        self.display_player_info(self.screen)
        # for hitbox in self.player.hitboxArray:
        #    pygame.draw.rect(self.screen, (255, 0, 0), hitbox, 3)
        pygame.display.update()

    def key_event(self, key):
        if self.player.health > 0:
            if key[pygame.K_DOWN] or key[pygame.K_s]:
                if self.player.ycor + self.player.playerSpeed < self.windowHeight - 70:
                    self.player.ycor += self.player.playerSpeed
                    for hitbox in self.player.hitboxArray:
                        hitbox[1] += self.player.playerSpeed
            if key[pygame.K_UP] or key[pygame.K_w]:
                if self.player.ycor - self.player.playerSpeed > 0:
                    self.player.ycor -= self.player.playerSpeed
                    for hitbox in self.player.hitboxArray:
                        hitbox[1] -= self.player.playerSpeed
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                if self.player.xcor + self.player.playerSpeed > 0:
                    self.player.xcor -= self.player.playerSpeed
                    for hitbox in self.player.hitboxArray:
                        hitbox[0] -= self.player.playerSpeed
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                if self.player.xcor + self.player.playerSpeed < self.windowWidth - 60:
                    self.player.xcor += self.player.playerSpeed
                    for hitbox in self.player.hitboxArray:
                        hitbox[0] += self.player.playerSpeed
            if key[pygame.K_SPACE]:
                if self.bulletTimer <= 0:
                    self.bulletTimer = self.player.fireRate
                    self.shoot_bullet()

    def game_over(self):
        return self.gameOver

    def display_player_info(self, screen):
        # displays player info
        count = 0
        spacing = 28
        player_health = self.player.health
        text = self.font.render('Score:' + str(self.player.score), False, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        while count < self.player.health * spacing:
            screen.blit(self.heart[0], (10 + count, 38))
            count += spacing
        while player_health != self.player.maxHealth:
            player_health += 1
            screen.blit(self.heart[1], (10 + count, 38))
            count += spacing

    def shoot_bullet(self):
        # player shoots bullet. shootType can be customized to change the starting position of the bullet and how many bullets shot
        if self.player.shootType == 'single_middle':
            bullet = Bullet(self.player.xcor + (self.player.rect.width / 2 - 5), self.player.ycor, self.player.currentBullet[1], self.player.currentBullet[2], self.player.currentBullet[3], 0, self.player)
            self.bulletArray.add(bullet)
            bullet.sound.play()
    # Use to determine where to spawn enemies and the type of enemies that come out in each spawn section.
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
            if i.ability(dt):
                if i.name == 'Imperier':
                    bullet = EnemyBullet(i.xcor + (i.rect.width / 2) - 15, i.ycor + i.height - 12,
                                    10, 24,
                                    'Sprites/Projectiles/Small_Enemy_Red_Bullet', 0, i.name, pygame.mixer.Sound('Sprites/Projectiles/Small_Red_Bullet.wav'), 3, 0)
                    self.enemyBulletArray.add(bullet)
                    bullet.sound.play()
                elif i.name == 'Impaler':
                    i.speed = 3
                elif i.name == 'Scatter':
                    bullet1 = EnemyBullet(i.xcor + (i.rect.width / 2) - 15, i.ycor + i.height - 12,
                                         10, 24,
                                         'Sprites/Projectiles/Small_Enemy_Red_Bullet', 0, i.name,
                                         pygame.mixer.Sound('Sprites/Projectiles/Small_Red_Bullet.wav'), 3, .5)
                    bullet2 = EnemyBullet(i.xcor + (i.rect.width / 2) - 15, i.ycor + i.height - 12,
                                         10, 24,
                                         'Sprites/Projectiles/Small_Enemy_Red_Bullet', 0, i.name,
                                         pygame.mixer.Sound('Sprites/Projectiles/Small_Red_Bullet.wav'), 3, -.5)
                    bullet3 = EnemyBullet(i.xcor + (i.rect.width / 2) - 15, i.ycor + i.height - 12,
                                         10, 24,
                                         'Sprites/Projectiles/Small_Enemy_Red_Bullet', 0, i.name,
                                         pygame.mixer.Sound('Sprites/Projectiles/Small_Red_Bullet.wav'), 3, 0)
                    self.enemyBulletArray.add(bullet1)
                    self.enemyBulletArray.add(bullet2)
                    self.enemyBulletArray.add(bullet3)
                    bullet1.sound.play()
                    bullet2.sound.play()
                    bullet3.sound.play()

            i.update(self.screen, dt)
            # Debug hitbox. Shows enemy hitboxes in red rectangle.
            # for hitbox in i.hitboxArray:
            #     pygame.draw.rect(self.screen, (255, 0, 0), hitbox, 3)
            # for hurtbox in i.hurtboxArray:
            #    pygame.draw.rect(self.screen, (0, 0, 255), hurtbox, 3)
            if i.ycor > self.windowHeight + 96:
                self.enemyList.remove(i)

    def move_bullets(self, dt):
        # moves all player bullets on the screen and removes them when they leave the screen
        for bullet in self.bulletArray:
            bullet.move()
            bullet.update(self.screen, dt)
            # pygame.draw.rect(self.screen, (0, 0, 255), bullet.hurtbox, 1)
            if bullet.ycor < -20:
                self.bulletArray.remove(bullet)
        for bullet in self.enemyBulletArray:
            bullet.move()
            bullet.update(self.screen, dt)
            # pygame.draw.rect(self.screen, (0, 0, 255), bullet.hurtbox, 1)
            if bullet.ycor > 770:
                self.enemyBulletArray.remove(bullet)

    def enemy_hit(self):
        global globalPlayerScore
        for enemy in self.enemyList:
            for bullet in self.bulletArray:
                for hitbox in enemy.hitboxArray:
                    if bullet.hurtbox[0] + bullet.hurtbox[2] > hitbox[0] and bullet.hurtbox[0] < hitbox[0] + hitbox[2]:
                        if bullet.hurtbox[1] + bullet.hurtbox[3] > hitbox[1] and bullet.hurtbox[1] < hitbox[1] + hitbox[3]:
                            enemy.health = enemy.health - self.player.damage
                            if enemy.health <= 0:
                                self.explosionArray.add(Explosion(enemy.xcor, enemy.ycor, enemy.width, enemy.height, enemy.explosion, 0, enemy.explosionSound))
                                self.player.score += enemy.score
                                globalPlayerScore = self.player.score
                                self.enemyList.remove(enemy)
                            else:
                                self.explosionArray.add(
                                    Explosion(bullet.xcor, bullet.ycor, bullet.explosionSize, bullet.explosionSize,
                                          bullet.explosionImages, 0, bullet.hitSound))
                            self.bulletArray.remove(bullet)
                            break

    def player_hit(self, dt):
        if self.player.invincible == False and self.player.health > 0:
            for hitbox in self.player.hitboxArray:
                for enemy in self.enemyList:
                    for hurtbox in enemy.hurtboxArray:
                        if hurtbox[0] + hurtbox[2] > hitbox[0] and hurtbox[0] < hitbox[0] + hitbox[2] and self.player.invincible == False:
                            if hurtbox[1] + hurtbox[3] > hitbox[1] and hurtbox[1] < hitbox[1] + hitbox[3] and self.player.invincible == False:
                                self.player.health -= 1
                                self.player.invincible = True
                for bullet in self.enemyBulletArray:
                    if bullet.hurtbox[0] + bullet.hurtbox[2] > hitbox[0] and bullet.hurtbox[0] < hitbox[0] + hitbox[2]:
                        if bullet.hurtbox[1] + bullet.hurtbox[3] > hitbox[1] and bullet.hurtbox[1] < hitbox[1] + hitbox[
                            3]:
                            self.player.health -= 1
                            self.player.invincible = True
                            self.enemyBulletArray.remove(bullet)
                            break
        elif self.player.health <= 0:
            self.player.invincible = False
            self.gameOver = self.player.dead
        else:
            if self.player.iFrames < self.player.collisionTime:
                self.player.invincible = False
                self.player.collisionTime = 0
            else:
                self.player.collisionTime += dt

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
    def __init__(self, xcor, ycor, width, height, images, starting_frame, shoot_type, name, des_images):
        super().__init__(xcor, ycor, width, height, images, starting_frame)

        self.shootType = shoot_type
        self.fireRate = .3
        self.playerSpeed = 7
        self.playerMaxSpeed = 7
        self.bulletSpeed = 10
        self.damage = 1
        self.maxHealth = 1 # original = 3
        self.health = 1 # original = 3
        self.score = 0
        self.dead = False
        self.iFrames = 1.5
        self.collisionTime = 0
        self.invincible = False
        self.des_images = View.load_images(des_images)
        self.smallBasicBullet = ['sm_basic_bullet', 10, 24, 'Sprites/Projectiles/Small_Basic_Bullet',
                                 pygame.mixer.Sound('Sprites/Projectiles/Basic_Bullet.wav'), 'Sprites/Explosions/16x16_Basic_Explosion', 16, pygame.mixer.Sound('Sprites/Projectiles/Basic_Bullet_Hit.wav')]
        self.currentBullet = self.smallBasicBullet
        self.name = name
        self.hitboxArray = []
        if self.name == 'Infinity':
            self.hitboxArray.append([self.xcor + 25, self.ycor, 15, 50])
            self.hitboxArray.append([self.xcor + 7, self.ycor + 30, 53, 15])

    def update_time_dependent(self, screen, dt):
        # Sprite flickers if invincible
        self.currentTime += dt
        if self.health > 0:
            if self.currentTime >= self.animationTime:
                self.currentTime = 0
                self.index = (self.index + 1) % len(self.images)
            if not self.invincible:
                screen.blit(self.images[self.index], (self.xcor, self.ycor))
            else:
                if self.index % 2:
                    screen.blit(self.images[self.index], (self.xcor, self.ycor))
        else:
            if self.currentTime >= self.animationTime:
                self.currentTime = 0
                self.index = (self.index + 1) % len(self.des_images)
                if self.index == len(self.des_images) - 1:
                    self.dead = True
                    self.kill()
            screen.blit(self.des_images[self.index], (self.xcor, self.ycor))



class Bullet(GameSprite):
    # bullet class (xcor, ycor, width, height, folder containing the images, starting frame, player)
    def __init__(self, xcor, ycor, width, height, images, starting_frame, player):
        super().__init__(xcor, ycor, width, height, images, starting_frame)
        self.player = player
        self.name = player.currentBullet[0]
        self.sound = player.currentBullet[4]
        self.hitSound = player.currentBullet[7]
        self.explosionImages = player.currentBullet[5]
        self.explosionSize = player.currentBullet[6]
        self.hurtbox = [self.xcor, self.ycor + 4, 10, 24]

    def move(self):
        # moves the bullet. can customize bullet pathing
        if self.name == 'sm_basic_bullet':
            self.ycor -= self.player.bulletSpeed
            self.hurtbox[1] -= self.player.bulletSpeed


class EnemyBullet(GameSprite):
    # bullet class (xcor, ycor, width, height, folder containing the images, starting frame, player)
    def __init__(self, xcor, ycor, width, height, images, starting_frame, enemy_name, sound, speed, x):
        super().__init__(xcor, ycor, width, height, images, starting_frame)
        self.name = enemy_name
        self.sound = sound
        self.hurtbox = [self.xcor + 10, self.ycor + 4, 12, 24]
        self.speed = speed
        self.x = x
        # self.angle = math.acos((speed**2)/((x**2+speed**2)*(speed**2)))
        # print(self.angle)
        # self.images = [pygame.transform.rotate(self.images[0], self.angle)]

    def move(self):
        # moves the bullet. can customize bullet pathing
        if self.name == 'Imperier':
            self.ycor += self.speed
            self.hurtbox[1] += self.speed
        elif self.name == 'Scatter':
            self.xcor += self.x
            self.ycor += self.speed
            self.hurtbox[0] += self.x
            self.hurtbox[1] += self.speed


class Explosion(GameSprite):
    def __init__(self, xcor, ycor, width, height, images, starting_frame, sound):
        super().__init__(xcor, ycor, width, height, images, starting_frame)
        self.sound = sound
        self.soundPlayed = False

    def update_time_dependent(self, screen, dt):
        # Updates the image of Sprite based on animation_time. Must provide: (the window, milliseconds since last frame)
        if not self.soundPlayed:
            self.sound.play()
            self.soundPlayed = True
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.index = (self.index + 1) % len(self.images)
            if self.index == len(self.images) - 1:
                self.kill()
        screen.blit(self.images[self.index], (self.xcor, self.ycor))


class Enemy(GameSprite):
    # enemy class (xcor, ycor, width, height, folder containing the images, starting frame, name of enemy, health, speed)
    def __init__(self, xcor, ycor, width, height, images, starting_frame, name, health, speed, score, abilitycd, explosion, explosion_sound):
        super().__init__(xcor, ycor, width, height, images, starting_frame)
        self.width = width
        self.height = height
        self.name = name
        self.speed = speed
        self.health = health
        self.score = score
        self.explosion = explosion
        self.explosionSound = explosion_sound
        self.hitboxArray = []
        self.abilitycd = abilitycd
        self.cd = self.abilitycd

        if self.name == 'Impaler':
            self.hitboxArray.append([self.xcor + 10, self.ycor + 20, 75, 30])
        elif self.name == 'Imperier':
            self.hitboxArray.append([self.xcor + 20, self.ycor + 10, 25, 50])
            self.hitboxArray.append([self.xcor + 1, self.ycor + 30, 62, 20])
        elif self.name == 'Scatter':
            self.hitboxArray.append([self.xcor + 27, self.ycor + 13, 10, 50])
            self.hitboxArray.append([self.xcor + 15, self.ycor + 25, 35, 20])
            self.hitboxArray.append([self.xcor, self.ycor + 20, 64, 20])

        self.hurtboxArray = copy.deepcopy(self.hitboxArray)
        if self.name == 'Impaler':
            self.hurtboxArray.append([self.xcor + 15, self.ycor + 50, 5, 40])
            self.hurtboxArray.append([self.xcor + 35, self.ycor + 50, 5, 40])
            self.hurtboxArray.append([self.xcor + 55, self.ycor + 50, 5, 40])
            self.hurtboxArray.append([self.xcor + 75, self.ycor + 50, 5, 40])


    def move(self):
        # moves the enemy. can customize enemy pathing
        if self.name == 'Impaler' or 'Imperier':
            self.ycor += self.speed
            for hitbox in self.hitboxArray:
                hitbox[1] += self.speed
            for hurtbox in self.hurtboxArray:
                hurtbox[1] += self.speed
        # self.hitbox = (self.xcor + 10, self.ycor + 10, self.hitboxX, self.hitboxY)

    def ability(self, dt):
        self.cd -= dt
        if self.cd <= 0:
            self.cd = self.abilitycd
            return True
        else:
            return False




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
        elif formation_type == 'scatter_v1':
            self.enemyGroup.append(self.create_enemy('Scatter', section.midPoint, section.yaxis))
            self.enemyGroup.append(self.create_enemy('Imperier', section.startPoint + 16, section.yaxis - 64))
            self.enemyGroup.append(self.create_enemy('Imperier', section.endPoint - 16, section.yaxis - 64))
        elif formation_type == 'scatter_^1':
            self.enemyGroup.append(self.create_enemy('Imperier', section.midPoint, section.yaxis - 64))
            self.enemyGroup.append(self.create_enemy('Scatter', section.startPoint + 16, section.yaxis))
            self.enemyGroup.append(self.create_enemy('Scatter', section.endPoint - 16, section.yaxis))
        elif formation_type == 'scatimp_^1':
            self.enemyGroup.append(self.create_enemy('Impaler', section.midPoint - 16, section.yaxis))
            self.enemyGroup.append(self.create_enemy('Scatter', section.startPoint, section.yaxis - 64))
            self.enemyGroup.append(self.create_enemy('Scatter', section.endPoint, section.yaxis - 64))

    def create_enemy(self, enemy, xcor, ycor):
        if enemy == 'Impaler':
            enemyShip = Enemy(xcor, ycor, 96, 96, 'Sprites/EnemyShips/Lvl1_Enemy_Impaler', 0, enemy, 3, 1.5, 150, random.uniform(1, 6), 'Sprites/Explosions/96x96_Explosion1', pygame.mixer.Sound('Sprites/Explosions/Explosion1.wav'))
        elif enemy == 'Imperier':
            enemyShip = Enemy(xcor, ycor, 64, 64, 'Sprites/EnemyShips/Lvl1_Enemy_Imperier', 0, enemy, 2, 1, 100, random.uniform(2, 6), 'Sprites/Explosions/64x64_Explosion1', pygame.mixer.Sound('Sprites/Explosions/Explosion1.wav'))
        elif enemy == 'Scatter':
            enemyShip = Enemy(xcor, ycor, 64, 64, 'Sprites/EnemyShips/Lvl1_Enemy_Scatter', 0, enemy, 2, 1, 250, random.uniform(2, 6), 'Sprites/Explosions/64x64_Explosion1', pygame.mixer.Sound('Sprites/Explosions/Explosion1.wav'))
        enemyShip.xcor = xcor
        enemyShip.ycor = ycor
        return enemyShip
