# importation for pygame and os
import pygame
import os


class View(object):
    #  parent class of view
    def __init__(self):
        self.running = True
        # Pygame window width
        self.windowWidth = 700
        # Pygame window height
        self.windowHeight = 750
        # Volume for sound effects and music
        self.soundEffectVolume = 0.5
        self.musicVolume = 0.5
        # Initializes pygame screen
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        # Frames for playership
        self.BasicShipFrames = View.load_images('PlayerShips')
        # Frames for stars
        self.star1 = View.load_images('Background/Animated_Star1')
        self.star2 = View.load_images('Background/Animated_Star2')
        self.star3 = View.load_images('Background/Animated_Star3')
        pygame.display.set_caption('BEYOND INFINITY')
        pygame.display.set_icon(pygame.image.load('PlayerShips/BasicShipFlying0.png'))

    def is_running(self):
        # returns running which either continues or stops the game
        return self.running

    @staticmethod
    def load_images(path):
        # loads images and returns the images in an array
        images = []
        for file_name in os.listdir(path):
            image = pygame.image.load(path + os.sep + file_name).convert()
            images.append(image)
        return images

    def transition(self):
        # plays select sound effect and screen fades out
        pygame.mixer.music.load('Menu/Menu_Select.mp3')
        pygame.mixer.music.play()
        fade = pygame.Surface((self.windowWidth, self.windowHeight))
        fade.fill((0, 0, 0))
        for alpha in range(0, 75):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(2)

    def play_music(self, path):
        # plays music on repeat. Must provide: (path of .wav file)
        music = pygame.mixer.Sound(path)
        music.set_volume(self.musicVolume)
        return music.play(-1)


class Sprite(pygame.sprite.Sprite):
    # class for a Sprite. To create a sprite you must provide: (x coordinate, y coordinate, size of the image, array of
    # all the images, and the starting frame)
    def __init__(self, xcor, ycor, size, images, starting_frame):
        super(Sprite, self).__init__()
        self.xcor = xcor
        self.ycor = ycor
        # creates rectangle for the sprite
        self.rect = pygame.Rect((xcor, ycor), (size, size))
        self.images = images
        # time it takes for the the sprite moves to the next frame
        self.animationTime = .08
        self.currentTime = 0
        self.index = starting_frame
        # 'image' is the current image of the animation.
        self.image = images[self.index]

    def update_time_dependent(self, screen, dt):
        # Updates the image of Sprite based on animation_time. Must provide: (the window, milliseconds since last frame)
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
        screen.blit(self.image, (self.xcor, self.ycor))

    def update(self, screen, dt):
        # This is the method that's being called when 'all_sprites.update(dt)' is called. Must provide:
        # (the window, milliseconds since last frame)
        self.update_time_dependent(screen, dt)


class PlayerShip(pygame.sprite.Sprite):
    # class for a Sprite. To create a sprite you must provide: (x coordinate, y coordinate, size of the image, array of
    # all the images, and the starting frame)
    def __init__(self, xcor, ycor, size, images, starting_frame):
        super(PlayerShip, self).__init__()
        self.xcor = xcor
        self.ycor = ycor
        # creates rectangle for the sprite
        self.rect = pygame.Rect((xcor, ycor), (size, size))
        self.images = images
        # time it takes for the the sprite moves to the next frame
        self.animationTime = .08
        self.currentTime = 0
        self.index = starting_frame
        # 'image' is the current image of the animation.
        self.image = images[self.index]
        self.xspeed = 4
        self.yspeed = 4

    def update_time_dependent(self, screen, dt):
        # Updates the image of Sprite based on animation_time. Must provide: (the window, milliseconds since last frame)
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
        screen.blit(self.image, (self.xcor, self.ycor))

    def update(self, screen, dt):
        # This is the method that's being called when 'all_sprites.update(dt)' is called. Must provide:
        # (the window, milliseconds since last frame)
        self.update_time_dependent(screen, dt)
