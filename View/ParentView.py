import pygame  # importation for pygame
import os


class View(object):
    def __init__(self):
        self.running = True
        # Pygame window width
        self.winWidth = 700
        # Pygame window height
        self.widHeight = 750
        # Initializes pygame screen
        self.screen = pygame.display.set_mode((self.winWidth, self.widHeight))
        # Frames for playership
        self.BasicShipFrames = View.load_images('PlayerShips')
        # Frames for stars
        self.star1 = View.load_images('Background/Animated_Star1')
        self.star2 = View.load_images('Background/Animated_Star2')
        self.star3 = View.load_images('Background/Animated_Star3')
        pygame.display.set_caption('BEYOND INFINITY')
        pygame.display.set_icon(pygame.image.load('PlayerShips/BasicShipFlying0.png'))

    def isRunning(self):
        return self.running

    @staticmethod
    def load_images(path):
        images = []
        for file_name in os.listdir(path):
            image = pygame.image.load(path + os.sep + file_name).convert()
            images.append(image)
        return images

    def transition(self):
        pygame.mixer.music.load('Menu/Menu_Select.mp3')
        pygame.mixer.music.play()
        fade = pygame.Surface((self.winWidth, self.widHeight))
        fade.fill((0, 0, 0))
        for alpha in range(0, 75):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(2)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, xcor, ycor, size, images, current_frame):
        super(Sprite, self).__init__()
        self.xcor = xcor
        self.ycor = ycor
        self.rect = pygame.Rect((xcor, ycor), (size, size))
        self.images = images
        self.animationTime = .08
        self.current_time = 0
        self.index = current_frame
        self.image = images[self.index]  # 'image' is the current image of the animation.

    # Updates the image of Sprite based on animation_time.
    def update_time_dependent(self, screen, dt):
        self.current_time += dt
        if self.current_time >= self.animationTime:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
        screen.blit(self.image, (self.xcor, self.ycor))

    # This is the method that's being called when 'all_sprites.update(dt)' is called
    def update(self, screen, dt):
        self.update_time_dependent(screen, dt)

