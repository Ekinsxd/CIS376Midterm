import pygame
from components.Tiles.DynamicTile import DynamicTile
from components.constants import FRAME_LIMIT

# Drawable, Updateable


# > This class is a subclass of DynamicTile, and it's a tile that can be interacted with
class MysteryBoxTile(DynamicTile):
    def __init__(self, image, x, y, spritesheet):
        """
        It takes an image, x and y coordinates, and a spritesheet, and then it sets the image to the
        image in the spritesheet, and then it sets the image to the blank image in the spritesheet.

        :param image: The name of the image in the spritesheet
        :param x: x position of the tile
        :param y: y position of the tile
        :param spritesheet: A dictionary of sprites
        """
        self.sprites = spritesheet[image]
        self.sprites.append(spritesheet['blank'])
        self.imageIndex = 0
        self.image = pygame.transform.scale(
            self.sprites[self.imageIndex], (32, 32))
        self.spent = False
        self.fadeFrame = 0
        super().__init__(None, x, y, None)

    def update(self, tiles):
        """
        If the player has collided with a tile, the player's image is set to the 6th image in the
        sprites list. If the player has not collided with a tile, the player's image is set to the next
        image in the sprites list

        :param tiles: a list of all the tiles in the game
        """
        if self.collided:
            self.imageIndex = 6
        elif self.fadeFrame == (FRAME_LIMIT):
            self.imageIndex = (self.imageIndex + 1) % 6
            self.fadeFrame = 0
        self.fadeFrame += 1
        self.image = pygame.transform.scale(
            self.sprites[self.imageIndex], (32, 32))
