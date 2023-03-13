import pygame
from components.Tiles.DynamicTile import DynamicTile
from components.constants import FRAME_LIMIT

# Drawable, Updateable


# It's a tile that can be
# touched by the player, and when it is, the player will win
class Flag(DynamicTile):
    def __init__(self, image, x, y, spritesheet):
        """
        It takes an image, x and y coordinates, and a spritesheet, and then it sets the sprite to the
        image in the spritesheet, scales it by 1.9, and then it calls the super() function.

        :param image: The image to be used
        :param x: x position of the sprite
        :param y: y-coordinate of the top left corner of the sprite
        :param spritesheet: A dictionary of sprites
        """
        self.sprite = spritesheet[image]
        self.image = pygame.transform.scale_by(
            self.sprite, 1.9)
        super().__init__(None, x, y, None)
