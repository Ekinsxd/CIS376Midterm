import pygame
from components.Tiles.DynamicTile import DynamicTile
from components.constants import FRAME_LIMIT

# Drawable, Updateable
class MysteryBoxTile(DynamicTile):
    def __init__(self, image, x, y, spritesheet):
        self.sprites = spritesheet[image]
        self.sprites.append(spritesheet['blank'])
        self.imageIndex = 0
        self.image = pygame.transform.scale(self.sprites[self.imageIndex], (32, 32))
        self.spent = False
        self.fadeFrame = 0
        super().__init__(None, x, y, None)


    def update(self):
        if self.collided:
            self.imageIndex = 6
        elif self.fadeFrame == (FRAME_LIMIT/3):
            self.imageIndex = (self.imageIndex + 1) % 6
            self.fadeFrame = 0
        self.fadeFrame += 1
        self.image = pygame.transform.scale(self.sprites[self.imageIndex], (32, 32))

