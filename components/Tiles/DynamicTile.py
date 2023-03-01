from components.Tiles.Tile import Tile
import components.mainScene as mainScene
import Box2D

class DynamicTile(Tile):
    def __init__(self, image, x, y, spritesheet):
        self.body = mainScene.Display.world.CreateDynamicBody(
            position=(x/100, (600 -32 - y) / 100),
            shapes = Box2D.b2PolygonShape(box=(0.32,0.32))
            )
        self.collided = False
        super().__init__(image, x, y, spritesheet)


    def collide(self):
        if (self.collided):
            return False
        self.collided = True
        return True