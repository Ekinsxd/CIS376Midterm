import pygame
from components.spritesheet import *


class Background(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet, scale):
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
        surface.blit(self.image, (self.rect.x, self.rect.y))
