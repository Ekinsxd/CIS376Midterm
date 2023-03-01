import pygame
from components.Tiles.DynamicTile import DynamicTile


# Drawable, Updateable
class BrickTile(DynamicTile):
    def __init__(self, image, x, y, spritesheet):
        self.sprites = [spritesheet[image]]
        self.sprites.append(spritesheet['blank'])
        self.image = pygame.transform.scale(self.sprites[0], (32, 32))
        super().__init__(None, x, y, None)


    def update(self):
        if self.collided:
            self.image = pygame.transform.scale(self.sprites[1], (32, 32))
