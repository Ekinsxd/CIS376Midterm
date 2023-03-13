from components.Tiles.Tile import Tile
import components.mainScene as mainScene
import Box2D


# DynamicTile is a Tile that can be moved.
class DynamicTile(Tile):
    def __init__(self, image, x, y, spritesheet):
        """
        It creates a dynamic body with a box shape of size 0.32x0.32 at position x,y
        
        :param image: The image to be used for the sprite
        :param x: x position of the object
        :param y: The y position of the object
        :param spritesheet: A pygame.Surface object that contains the spritesheet
        """
        self.body = mainScene.Display.world.CreateDynamicBody(
            position=(x/100, (600 - 32 - y) / 100),
            shapes=Box2D.b2PolygonShape(box=(0.32, 0.32))
        )
        self.collided = False
        super().__init__(image, x, y, spritesheet)

    def collide(self, playerBig=None):
        """
        If the player has collided with an object, return False. If the player has not collided with an
        object, set the player's collided variable to True and return True
        
        :param playerBig: The player's current size
        :return: The return value is a boolean value.
        """
        if self.collided:
            return False
        self.collided = True
        return True
