from components.Tiles.Tile import Tile
import components.mainScene as mainScene
import Box2D


class StaticTile(Tile):
    # StaticTile is a Tile that has a static image.
    def __init__(self, image, x, y, spritesheet):
        """
        It creates a static body at the position of the sprite, and then calls the superclass's
        constructor.
        
        :param image: The image to be used for the sprite
        :param x: x position of the object
        :param y: y position of the object
        :param spritesheet: A pygame.Surface object that contains the spritesheet
        """
        self.body = mainScene.Display.world.CreateStaticBody(
            position=(x/100, (600 -32 - y) / 100),
            shapes = Box2D.b2PolygonShape(box=(0.32,0.32))
            )
        super().__init__(image, x, y, spritesheet)