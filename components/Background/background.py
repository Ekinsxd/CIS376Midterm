import pygame
from components.spritesheet import *


# This class is a subclass of the pygame.sprite.Sprite class
class Background(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet, scale):
        """
        It takes in an image, x and y coordinates, a spritesheet, and a scale, and then it loads the
        image from the spritesheet, scales it, and then sets the x and y coordinates

        :param image: The name of the image in the spritesheet
        :param x: x position of the sprite
        :param y: y-coordinate
        :param spritesheet: A dictionary of images
        :param scale: The scale of the image
        """
        pygame.sprite.Sprite.__init__(self)
        if image != None and spritesheet != None:
            self.image = spritesheet[image]
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
            self.image = pygame.transform.scale_by(
                spritesheet[image], scale)

        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        """
        It takes the image and the rect of the sprite and draws it to the surface

        :param surface: The surface to draw the image on
        """
        surface.blit(self.image, (self.rect.x, self.rect.y))
