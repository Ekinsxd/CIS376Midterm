import pygame
from components.Tiles.DynamicTile import DynamicTile
from components.constants import FRAME_LIMIT

# Drawable, Updateable


class Flag(DynamicTile):
    def __init__(self, image, x, y, spritesheet):
        self.sprite = spritesheet[image]
        self.image = pygame.transform.scale_by(
            self.sprite, 1.9)
        super().__init__(None, x, y, None)

    def update(self, tiles):
        pass

    def collide(self, player):
        if self.collided:
            # trigger win
            return True
        return False
