from components.Tiles.DynamicTile import DynamicTile
from components.constants import SKY_BLUE

# Drawable, Updateable
# > A brick tile is a dynamic tile that can be destroyed by the player
class BrickTile(DynamicTile):
    def __init__(self, image, x, y, spritesheet):
        """
        The function __init__ is a constructor that takes in the parameters image, x, y, and spritesheet
        and calls the super class constructor with the same parameters
        
        :param image: The image of the sprite
        :param x: The x coordinate of the top left corner of the sprite
        :param y: The y coordinate of the top left corner of the sprite
        :param spritesheet: The spritesheet that the image is on
        """
        super().__init__(image, x, y, spritesheet)


    def update(self, tiles):
        """
        If the player has collided with a tile, and the tile is in the list of tiles, then fill the tile
        with sky blue and remove it from the list of tiles
        
        :param tiles: a list of all the tiles in the game
        """
        if self.collided and tiles.count(self) > 0:
            self.image.fill(SKY_BLUE)
            tiles.remove(self)


    def collide(self, playerBig=None):
        """
        If the player is big, then the enemy is collided
        
        :param playerBig: If the player is big or not
        :return: False
        """
        if (not self.collided) and playerBig != None:
            self.collided = True if playerBig else False
        return False

