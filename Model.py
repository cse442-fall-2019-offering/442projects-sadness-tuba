import pygame  # importation for pygame


class MenuOption(object):

    def __init__(self, name, unhighlighted, highlighted, imgWidth, yAxisImageSpacing):
        self.name = name
        self.unhighlighted = unhighlighted
        self.highlighted = highlighted
        self.imgWidth = imgWidth
        self.yAxisImageSpacing = yAxisImageSpacing


#  option class (button name, image, highlighted image, image width, height spacing between each image)
#  If you want to add one more option, add 75 to height spacing between each image
# 346x44
startOption = MenuOption("start", pygame.image.load('../Options/Start_Game.png'), pygame.image.load('../Options/Start_Game_Highlighted.png'), 346, 0)
# 146x44
shopOption = MenuOption("shop", pygame.image.load('../Options/Shop.png'), pygame.image.load('../Options/Shop_Highlighted.png'), 146, 0)
# 274x44
settingsOption = MenuOption("settings", pygame.image.load('../Options/Settings.png'), pygame.image.load('../Options/Settings_Highlighted.png'), 274, 0)
# 126x44
quitOption = MenuOption("quit", pygame.image.load('../Options/Quit.png'), pygame.image.load('../Options/Quit_Highlighted.png'), 126, 0)
# Selected option is the  option the user has selected. This will be used to determine when the image becomes
# highlighted
selectedOption = startOption

# a tuple that stores all the men option tuples
optionTuple = (startOption, shopOption, settingsOption, quitOption)


class PlayerShip(pygame.sprite.Sprite):
    # Need to initialize class by defining its properties
    def __init__(self, xcor, ycor, ship_frames, width, height, animation_time, current_frame):
        super(PlayerShip, self).__init__()
        self.xcor = xcor
        self.ycor = ycor
        self.width = width
        self.height = height
        self.ship_frames = ship_frames
        self.animation_time = animation_time
        self.index = current_frame
        self.ship_frame = ship_frames[self.index]
        self.current_time = 0

    # Updates the image of Sprite based on animation_time.
    def update_time_dependent(self, dt, window):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.ship_frames)
            self.ship_frame = self.ship_frames[self.index]
        window.blit(self.ship_frame, (self.xcor, self.ycor))

    # This is the method that's being called when 'all_sprites.update(dt)' is called
    def update(self, dt, window):
        self.update_time_dependent(dt, window)


class AnimatedBackgroundSprite(pygame.sprite.Sprite):
    def __init__(self, xcor, ycor, images, size, animation_time, current_frame):
        super(AnimatedBackgroundSprite, self).__init__()
        self.xcor = xcor
        self.ycor = ycor
        position = (xcor, ycor)
        self.size = size
        self.rect = pygame.Rect(position, (size, size))
        self.images = images
        self.index = current_frame
        self.image = images[self.index]  # 'image' is the current image of the animation.
        self.animation_time = animation_time
        self.current_time = 0

    # Updates the image of Sprite based on animation_time.
    def update_time_dependent(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    # This is the method that's being called when 'all_sprites.update(dt)' is called
    def update(self, dt):
        self.update_time_dependent(dt)
