# importation for pygame and os
import copy
import random
import pygame
import math
from View.ParentView import View


# Class for defining the gameplay portion
class GameplayView(View):
    def __init__(self):
        super(GameplayView, self).__init__()
        self.name = "Gameplay"
        self.bg = pygame.image.load('Sprites/Menu/Blank_Page.png')
        # creates player class
        self.player = Player(310, 600, 64, 64, 'Sprites/PlayerShips/Infinity/Infinity_Flying', 0, 'single_middle',
                             'Infinity', 'Sprites/PlayerShips/Infinity/Infinity_Destroyed',
                             'Sprites/PlayerShips/Infinity/Power_Up', 'Ion_Blast')
        # List of each bullet
        self.bulletArray = pygame.sprite.Group()
        self.enemyBulletArray = pygame.sprite.Group()
        self.bulletTimer = 0
        self.explosionArray = pygame.sprite.Group()
        # Sections
        self.section1 = Section(1, 0, 180, -96, 6, 9, 1)
        self.section2 = Section(2, 244, 392, -96, 6, 9, 5)
        self.section3 = Section(3, 456, 636, -96, 6, 9, 1)
        self.sectionArray = [self.section1, self.section2, self.section3]
        # Enemy Formation ['imp_v1', 'impaler_diagonal1', 'impaler_diagonal2', 'imperier_v1', 'imperier_^1',
        # 'scatter_v1', 'scatter_^1', 'scatimp_^1', 'KZBomber_diagonal1', 'KZBomber_diagonal1']
        self.formationTypes = ['imp_v1', 'impaler_diagonal1', 'impaler_diagonal2', 'imperier_v1', 'imperier_^1',
                               'scatter_v1', 'scatter_^1', 'scatimp_^1', 'KZBomber_^1', 'KZBomber_v1']
        self.enemyList = pygame.sprite.Group()
        # Display
        self.heart = View.load_images('Sprites/Player_Info/Heart')
        self.allFonts = pygame.font.get_fonts()
        self.font = pygame.font.SysFont(self.allFonts[8], 24)
        self.font1 = pygame.font.SysFont(self.allFonts[8], 20)

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
        self.check_player_hit(dt)
        self.player.update(self.screen, dt)
        for j in self.explosionArray:
            j.update(self.screen, dt)
        self.display_player_info(self.screen)
        # Player Hitbox
        # for hitbox in self.player.hitboxArray:
        #  pygame.draw.rect(self.screen, (255, 0, 0), hitbox, 3)
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
            if key[pygame.K_e]:
                if self.player.energy == 100:
                    self.bulletTimer = self.player.fireRate
                    self.player.energy = 0
                    self.use_ability()

    def game_over(self):
        return self.gameOver

    def get_score(self):
        return self.player.score

    def display_player_info(self, screen):
        # displays player info
        count = 0
        spacing = 28
        player_health = self.player.health
        score_text = self.font.render('Score:' + str(self.player.score), False, (255, 255, 255))
        energy_text = self.font1.render(str(self.player.energy) + '%', False, (255, 255, 255))
        self.screen.blit(score_text, (15, 10))
        while count < self.player.health * spacing:
            screen.blit(self.heart[0], (10 + count, 38))
            count += spacing
        while player_health != self.player.maxHealth:
            player_health += 1
            screen.blit(self.heart[1], (10 + count, 38))
            count += spacing
        pygame.draw.rect(self.screen, (7, 82, 184), [15, 75, self.player.energy, 25], 0)
        pygame.draw.rect(self.screen, (255, 255, 255), [15, 75, 100, 25], 2)
        if self.player.energy < 10:
            self.screen.blit(energy_text, (55, 80))
        elif self.player.energy < 100:
            self.screen.blit(energy_text, (50, 80))
        else:
            self.screen.blit(energy_text, (45, 80))

    def shoot_bullet(self):
        # player shoots bullet. shootType can be customized to change the starting position of the bullet and how many bullets shot
        if self.player.shootType == 'single_middle':
            bullet = Bullet(self.player.xcor + (self.player.rect.width / 2 - 5), self.player.ycor,
                            self.player.currentBullet[1], self.player.currentBullet[2], self.player.currentBullet[3], 0,
                            self.player, self.player.currentBullet)
            self.bulletArray.add(bullet)
            bullet.sound.play()

    def use_ability(self):
        # player shoots bullet. shootType can be customized to change the starting position of the bullet and how many bullets shot
        if self.player.ability == 'Ion_Blast':
            bullet = Bullet(self.player.xcor, self.player.ycor, self.player.ionBlast[1], self.player.ionBlast[2],
                            self.player.ionBlast[3], 0, self.player, self.player.ionBlast)
            self.bulletArray.add(bullet)
            bullet.sound.play()

    def create_enemy(self, enemy, xcor, ycor):
        if enemy == 'Impaler':
            enemyShip = Enemy(xcor, ycor, 96, 96, 'Sprites/EnemyShips/Lvl1_Enemy_Impaler', 0, enemy, 3, 1.5, 150,
                              random.uniform(1, 4), 'Sprites/Explosions/96x96_Explosion1',
                              pygame.mixer.Sound('Sprites/Explosions/Explosion1.wav'), 96)
        elif enemy == 'Imperier':
            enemyShip = Enemy(xcor, ycor, 96, 96, 'Sprites/EnemyShips/Lvl1_Enemy_Imperier', 0, enemy, 2, 1, 100,
                              random.uniform(2, 7), 'Sprites/Explosions/64x64_Explosion1',
                              pygame.mixer.Sound('Sprites/Explosions/Explosion1.wav'), 64)
        elif enemy == 'Scatter':
            enemyShip = Enemy(xcor, ycor, 64, 64, 'Sprites/EnemyShips/Lvl1_Enemy_Scatter', 0, enemy, 2, 1, 250,
                              random.uniform(2, 7), 'Sprites/Explosions/64x64_Explosion1',
                              pygame.mixer.Sound('Sprites/Explosions/Explosion1.wav'), 64)
        elif enemy == 'KZBomber':
            enemyShip = Enemy(xcor, ycor, 64, 64, 'Sprites/EnemyShips/Lvl1_Enemy_KZ_Bomber', 0, enemy, 1, 1.5, 50, 0,
                              'Sprites/Explosions/128x128_Red_Explosion',
                              pygame.mixer.Sound('Sprites/Explosions/Explosion2.wav'), 128)
        enemyShip.xcor = xcor
        enemyShip.ycor = ycor
        return enemyShip

    # Use to determine where to spawn enemies and the type of enemies that come out in each spawn section.
    def spawn_enemies(self, section, dt):
        section.CD -= dt
        if section.CD <= 0:
            section.CD = random.uniform(section.earliestCD, section.latestCD)
            chosenFormation = random.choice(self.formationTypes)
            if chosenFormation == 'imp_v1':
                self.enemyList.add(self.create_enemy('Impaler', section.midPoint - 16, section.yaxis))
                self.enemyList.add(self.create_enemy('Imperier', section.startPoint, section.yaxis - 64))
                self.enemyList.add(self.create_enemy('Imperier', section.endPoint, section.yaxis - 64))
            elif chosenFormation == 'impaler_diagonal1':
                self.enemyList.add(self.create_enemy('Impaler', section.startPoint, section.yaxis))
                self.enemyList.add(self.create_enemy('Impaler', section.endPoint - 32, section.yaxis - 64))
            elif chosenFormation == 'impaler_diagonal2':
                self.enemyList.add(self.create_enemy('Impaler', section.startPoint, section.yaxis - 64))
                self.enemyList.add(self.create_enemy('Impaler', section.endPoint - 32, section.yaxis))
            elif chosenFormation == 'imperier_v1':
                self.enemyList.add(self.create_enemy('Imperier', section.midPoint, section.yaxis))
                self.enemyList.add(self.create_enemy('Imperier', section.startPoint + 16, section.yaxis - 64))
                self.enemyList.add(self.create_enemy('Imperier', section.endPoint - 16, section.yaxis - 64))
            elif chosenFormation == 'imperier_^1':
                self.enemyList.add(self.create_enemy('Imperier', section.midPoint, section.yaxis - 64))
                self.enemyList.add(self.create_enemy('Imperier', section.startPoint + 16, section.yaxis))
                self.enemyList.add(self.create_enemy('Imperier', section.endPoint - 16, section.yaxis))
            elif chosenFormation == 'scatter_v1':
                self.enemyList.add(self.create_enemy('Scatter', section.midPoint, section.yaxis))
                self.enemyList.add(self.create_enemy('Imperier', section.startPoint + 16, section.yaxis - 64))
                self.enemyList.add(self.create_enemy('Imperier', section.endPoint - 16, section.yaxis - 64))
            elif chosenFormation == 'scatter_^1':
                self.enemyList.add(self.create_enemy('Imperier', section.midPoint, section.yaxis - 64))
                self.enemyList.add(self.create_enemy('Scatter', section.startPoint + 16, section.yaxis))
                self.enemyList.add(self.create_enemy('Scatter', section.endPoint - 16, section.yaxis))
            elif chosenFormation == 'scatimp_^1':
                self.enemyList.add(self.create_enemy('Impaler', section.midPoint - 16, section.yaxis))
                self.enemyList.add(self.create_enemy('Scatter', section.startPoint, section.yaxis - 64))
                self.enemyList.add(self.create_enemy('Scatter', section.endPoint, section.yaxis - 64))
            elif chosenFormation == 'KZBomber_^1':
                self.enemyList.add(self.create_enemy('KZBomber', section.midPoint - 16, section.yaxis))
                self.enemyList.add(self.create_enemy('KZBomber', section.startPoint, section.yaxis - 64))
                self.enemyList.add(self.create_enemy('KZBomber', section.endPoint, section.yaxis - 64))
            elif chosenFormation == 'KZBomber_v1':
                self.enemyList.add(self.create_enemy('KZBomber', section.midPoint, section.yaxis))
                self.enemyList.add(self.create_enemy('KZBomber', section.startPoint + 16, section.yaxis - 64))
                self.enemyList.add(self.create_enemy('KZBomber', section.endPoint - 16, section.yaxis - 64))

    def move_enemies(self, dt):
        # moves all enemies on the screen and removes them when they leave the screen
        for i in self.enemyList:
            i.move(self.windowWidth)
            # enemy abilities
            if i.ability(dt):
                if i.name == 'Imperier':
                    bullet = EnemyBullet(i.xcor + (i.rect.width / 2) - 15, i.ycor + i.height - 12,
                                         10, 24,
                                         'Sprites/Projectiles/Small_Enemy_Red_Bullet', 0, 'small_red_bullet', i.name,
                                         pygame.mixer.Sound('Sprites/Projectiles/Small_Red_Bullet.wav'), 3, 0)
                    self.enemyBulletArray.add(bullet)
                    bullet.sound.play()
                elif i.name == 'Impaler':
                    i.speed = 3
                elif i.name == 'Scatter':
                    bullet1 = EnemyBullet(i.xcor + (i.rect.width / 2) - 15, i.ycor + i.height - 12,
                                          10, 24,
                                          'Sprites/Projectiles/Small_Enemy_Red_Bullet', 0, 'small_red_bullet', i.name,
                                          pygame.mixer.Sound('Sprites/Projectiles/Small_Red_Bullet.wav'), 3, .5)
                    bullet2 = EnemyBullet(i.xcor + (i.rect.width / 2) - 15, i.ycor + i.height - 12,
                                          10, 24,
                                          'Sprites/Projectiles/Small_Enemy_Red_Bullet', 0, 'small_red_bullet', i.name,
                                          pygame.mixer.Sound('Sprites/Projectiles/Small_Red_Bullet.wav'), 3, -.5)
                    bullet3 = EnemyBullet(i.xcor + (i.rect.width / 2) - 15, i.ycor + i.height - 12,
                                          10, 24,
                                          'Sprites/Projectiles/Small_Enemy_Red_Bullet', 0, 'small_red_bullet', i.name,
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
            #    pygame.draw.rect(self.screen, (255, 0, 0), hitbox, 3)
            # for hurtbox in i.hurtboxArray:
            #    pygame.draw.rect(self.screen, (0, 0, 255), hurtbox, 3)
            if i.ycor > self.windowHeight + 96:
                self.enemyList.remove(i)

    def move_bullets(self, dt):
        # moves all player bullets on the screen and removes them when they leave the screen shows bullet hurtbox
        for bullet in self.bulletArray:
            bullet.move()
            bullet.update(self.screen, dt)
            # shows player bullet hitbox
            # pygame.draw.rect(self.screen, (0, 0, 255), bullet.hurtbox, 1)
            if bullet.ycor < -20 or bullet.ycor > 770:
                self.bulletArray.remove(bullet)
        for bullet in self.enemyBulletArray:
            bullet.move()
            bullet.update(self.screen, dt)
            # shows enemy bullet hitbox
            # pygame.draw.rect(self.screen, (0, 0, 255), bullet.hurtbox, 1)
            if bullet.ycor < -20 or bullet.ycor > 770:
                self.enemyBulletArray.remove(bullet)

    def check_hit(self, hurtbox, hitbox):
        if hurtbox[0] + hurtbox[2] > hitbox[0] and hurtbox[0] < hitbox[0] + hitbox[2]:
            if hurtbox[1] + hurtbox[3] > hitbox[1] and hurtbox[1] < hitbox[1] + hitbox[3]:
                return True
        return False

    def enemy_hit(self):
        for enemy in self.enemyList:
            for bullet in self.bulletArray:
                for hitbox in enemy.hitboxArray:
                    if self.check_hit(bullet.hurtbox, hitbox):
                        enemy.health = enemy.health - bullet.damage
                        self.player.energy += 100
                        if bullet.explode:
                            self.explosionArray.add(
                                Explosion(bullet.xcor - ((bullet.explosionSize / 2) - (bullet.width / 2)),
                                          bullet.ycor - ((bullet.explosionSize / 2) - (bullet.height / 2)),
                                          bullet.explosionSize, bullet.explosionSize,
                                          bullet.explosionImages, 0, bullet.hitSound, True, True))
                        if enemy.health <= 0:
                            if enemy.explosionSize != enemy.width:
                                if enemy.category == 'explode':
                                    self.explosionArray.add(
                                        Explosion(enemy.xcor - (enemy.explosionSize / 2 - enemy.width / 2) / 2,
                                                  enemy.ycor,
                                                  enemy.explosionSize, enemy.explosionSize, enemy.explosion, 0,
                                                  enemy.explosionSound, True, False))
                                else:
                                    self.explosionArray.add(
                                        Explosion(enemy.xcor - (enemy.explosionSize - enemy.width) / 2, enemy.ycor,
                                                  enemy.explosionSize, enemy.explosionSize, enemy.explosion, 0,
                                                  enemy.explosionSound, False, True))
                            else:
                                self.explosionArray.add(
                                    Explosion(enemy.xcor, enemy.ycor, enemy.explosionSize, enemy.explosionSize,
                                              enemy.explosion, 0, enemy.explosionSound, False, True))
                            self.player.score += enemy.score
                            self.enemyList.remove(enemy)
                        else:
                            if not bullet.explode:
                                self.explosionArray.add(
                                    Explosion(bullet.xcor, bullet.ycor, bullet.explosionSize, bullet.explosionSize,
                                              bullet.explosionImages, 0, bullet.hitSound, False, True))
                        if self.player.energy > 100:
                            self.player.energy = 100
                        self.bulletArray.remove(bullet)
                        break

    def check_player_hit(self, dt):
        if self.player.invincible == False and self.player.health > 0:
            for hitbox in self.player.hitboxArray:
                for enemy in self.enemyList:
                    for hurtbox in enemy.hurtboxArray:
                        if self.check_hit(hurtbox, hitbox):
                            self.player_hit()
                            if enemy.category == 'explode':
                                self.explosionArray.add(
                                    Explosion(enemy.xcor - (enemy.explosionSize - enemy.width) / 2, enemy.ycor,
                                              enemy.explosionSize, enemy.explosionSize, enemy.explosion, 0,
                                              enemy.explosionSound, True, False))
                                self.enemyList.remove(enemy)
                            break
                for bullet in self.enemyBulletArray:
                    if self.check_hit(bullet.hurtbox, hitbox):
                        self.player_hit()
                        self.enemyBulletArray.remove(bullet)
                        break
                for explosion in self.explosionArray:
                    for hurtbox in explosion.hurtboxArray:
                        if explosion.damageable:
                            # Shows explosion hurtbox
                            # pygame.draw.rect(self.screen, (0, 0, 255), hurtbox, 3)
                            if self.check_hit(hurtbox, hitbox) and not explosion.friendly:
                                self.player_hit()
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

    def player_hit(self):
        self.player.health -= 1
        self.player.invincible = True
        self.player.hitSound.play()


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
    def __init__(self, xcor, ycor, width, height, images, starting_frame, shoot_type, name, des_images, power_images,
                 ability):
        super().__init__(xcor, ycor, width, height, images, starting_frame)

        self.shootType = shoot_type
        self.fireRate = .3
        self.playerSpeed = 7
        self.bulletSpeed = 10
        self.damage = 1
        self.maxHealth = 3
        self.health = 3
        self.score = 0
        self.energyGain = 4
        self.energy = 100
        self.ability = ability
        self.dead = False
        self.deathSoundPlayed = False
        self.iFrames = 1.5
        self.collisionTime = 0
        self.invincible = False
        self.des_images = View.load_images(des_images)
        self.smallBasicBullet = ['sm_basic_bullet', 10, 24, 'Sprites/Projectiles/Small_Basic_Bullet',
                                 pygame.mixer.Sound('Sprites/Projectiles/Basic_Bullet.wav'),
                                 'Sprites/Explosions/16x16_Basic_Explosion', 16,
                                 pygame.mixer.Sound('Sprites/Projectiles/Basic_Bullet_Hit.wav')]
        self.ionBlast = ['ion_blast', 64, 64, 'Sprites/Projectiles/Blue_Ion_Blast',
                         pygame.mixer.Sound('Sprites/Projectiles/Basic_Bullet.wav'),
                         'Sprites/Explosions/176x176_Blue_Explosion', 176,
                         pygame.mixer.Sound('Sprites/Projectiles/Basic_Bullet_Hit.wav')]
        self.name = name
        self.hitSound = pygame.mixer.Sound('Sprites/PlayerShips/Ship_Hit.wav')
        self.deathSound = pygame.mixer.Sound('Sprites/Explosions/Multiple_Explosions.wav')
        self.hitboxArray = []
        if self.name == 'Infinity':
            self.currentBullet = self.smallBasicBullet
            self.hitboxArray.append([self.xcor + 25, self.ycor, 15, 50])
            self.hitboxArray.append([self.xcor + 7, self.ycor + 35, 53, 10])

    def update_time_dependent(self, screen, dt):
        self.currentTime += dt
        if self.health > 0:
            if self.currentTime >= self.animationTime:
                self.currentTime = 0
                self.index = (self.index + 1) % len(self.images)
            # Sprite flickers if invincible
            if not self.invincible:
                screen.blit(self.images[self.index], (self.xcor, self.ycor))
            else:
                if self.index % 2:
                    screen.blit(self.images[self.index], (self.xcor, self.ycor))
        # Sprite dead animation
        else:
            if not self.deathSoundPlayed:
                self.deathSound.play()
                self.deathSoundPlayed = True
            if self.currentTime >= self.animationTime:
                self.currentTime = 0
                self.index = (self.index + 1) % len(self.des_images)
                if self.index == len(self.des_images) - 1:
                    self.dead = True
                    self.kill()
            screen.blit(self.des_images[self.index], (self.xcor, self.ycor))


class Bullet(GameSprite):
    # bullet class (xcor, ycor, width, height, folder containing the images, starting frame, player)
    def __init__(self, xcor, ycor, width, height, images, starting_frame, player, player_bullet):
        super().__init__(xcor, ycor, width, height, images, starting_frame)
        self.player = player
        self.width = width
        self.height = height
        self.name = player_bullet[0]
        self.sound = player_bullet[4]
        self.hitSound = player_bullet[7]
        self.explosionImages = player_bullet[5]
        self.explosionSize = player_bullet[6]
        self.explode = False

        if self.name == 'sm_basic_bullet':
            self.damage = self.player.damage
            self.hurtbox = [self.xcor, self.ycor + 4, 10, 24]
        elif self.name == 'ion_blast':
            self.explode = True
            self.damage = 3
            self.hurtbox = [self.xcor + 24, self.ycor + 24, 16, 16]

    def move(self):
        # moves the bullet. can customize bullet pathing
        if self.name == 'sm_basic_bullet':
            self.ycor -= self.player.bulletSpeed
            self.hurtbox[1] -= self.player.bulletSpeed
        elif self.name == 'ion_blast':
            self.ycor -= 4
            self.hurtbox[1] -= 4


class EnemyBullet(GameSprite):
    # bullet class (xcor, ycor, width, height, folder containing the images, starting frame, player)
    def __init__(self, xcor, ycor, width, height, images, starting_frame, bullet_name, enemy_name, sound, speed, x):
        super().__init__(xcor, ycor, width, height, images, starting_frame)
        self.bulletName = bullet_name
        self.name = enemy_name
        self.sound = sound
        self.hurtbox = [self.xcor + 10, self.ycor + 4, 12, 24]
        self.speed = speed
        self.x = x

        if self.bulletName == 'small_red_bullet':
            self.hurtbox = [self.xcor + 10, self.ycor + 4, 12, 24]

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
    def __init__(self, xcor, ycor, width, height, images, starting_frame, sound, damageable, friendly):
        super().__init__(xcor, ycor, width, height, images, starting_frame)
        self.sound = sound
        self.soundPlayed = False
        self.hurtboxArray = []
        self.damageable = damageable
        self.friendly = friendly

        if damageable:
            if width == 128:
                self.hurtboxArray.append([self.xcor + 56, self.ycor, 16, 128])
                self.hurtboxArray.append([self.xcor, self.ycor + 56, 128, 16])
                self.hurtboxArray.append([self.xcor + 20, self.ycor + 20, 87, 87])
            elif width == 176:
                self.hurtboxArray.append([self.xcor + 64, self.ycor, 48, 176])
                self.hurtboxArray.append([self.xcor, self.ycor + 64, 176, 48])
                self.hurtboxArray.append([self.xcor + 24, self.ycor + 24, 128, 128])

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
    def __init__(self, xcor, ycor, width, height, images, starting_frame, name, health, speed, score, abilitycd,
                 explosion, explosion_sound, explosion_size):
        super().__init__(xcor, ycor, width, height, images, starting_frame)
        self.width = width
        self.height = height
        self.name = name
        self.speed = speed
        self.health = health
        self.score = score
        self.explosion = explosion
        self.explosionSound = explosion_sound
        self.explosionSize = explosion_size
        self.hitboxArray = []
        self.abilitycd = abilitycd
        self.cd = self.abilitycd
        self.bool = bool(random.getrandbits(1))
        self.category = 'normal'
        if self.name == 'KZBomber':
            self.category = 'explode'

        if self.name == 'Impaler':
            self.hitboxArray.append([self.xcor + 10, self.ycor + 20, 75, 30])
        elif self.name == 'Imperier':
            self.hitboxArray.append([self.xcor + 20, self.ycor + 10, 25, 50])
            self.hitboxArray.append([self.xcor + 5, self.ycor + 35, 55, 10])
        elif self.name == 'Scatter':
            self.hitboxArray.append([self.xcor + 27, self.ycor + 13, 10, 50])
            self.hitboxArray.append([self.xcor + 15, self.ycor + 25, 35, 20])
            self.hitboxArray.append([self.xcor, self.ycor + 20, 64, 20])
        elif self.name == 'KZBomber':
            self.hitboxArray.append([self.xcor + 5, self.ycor + 30, 55, 10])
            self.hitboxArray.append([self.xcor + 12, self.ycor + 10, 40, 45])

        self.hurtboxArray = copy.deepcopy(self.hitboxArray)
        if self.name == 'Impaler':
            self.hurtboxArray.append([self.xcor + 15, self.ycor + 50, 5, 40])
            self.hurtboxArray.append([self.xcor + 35, self.ycor + 50, 5, 40])
            self.hurtboxArray.append([self.xcor + 55, self.ycor + 50, 5, 40])
            self.hurtboxArray.append([self.xcor + 75, self.ycor + 50, 5, 40])

    def move(self, windowWidth):
        # moves the enemy. can customize enemy pathing
        if self.name == 'KZBomber':
            self.ycor += self.speed
            if self.xcor >= windowWidth - self.width:
                self.bool = True
            elif self.xcor <= 0:
                self.bool = False
            if not self.bool:
                self.xcor += self.speed / 2
            else:
                self.xcor -= self.speed / 2
            for hitbox in self.hitboxArray:
                hitbox[1] += self.speed
                if not self.bool:
                    hitbox[0] += self.speed / 2
                else:
                    hitbox[0] -= self.speed / 2
            for hurtbox in self.hurtboxArray:
                hurtbox[1] += self.speed
                if not self.bool:
                    hurtbox[0] += self.speed / 2
                else:
                    hurtbox[0] -= self.speed / 2
        else:
            self.ycor += self.speed
            for hitbox in self.hitboxArray:
                hitbox[1] += self.speed
            for hurtbox in self.hurtboxArray:
                hurtbox[1] += self.speed

    def ability(self, dt):
        if not self.abilitycd == 0:
            self.cd -= dt
            if self.cd <= 0:
                self.cd = self.abilitycd
                return True
            else:
                return False
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
