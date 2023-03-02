from components.Tiles.DynamicTile import DynamicTile
from components.constants import SKY_BLUE

# Drawable, Updateable
class BrickTile(DynamicTile):
    def __init__(self, image, x, y, spritesheet):
        super().__init__(image, x, y, spritesheet)


    def update(self, tiles):
        if self.collided and tiles.count(self) > 0:
            self.image.fill(SKY_BLUE)
            tiles.remove(self)


    def collide(self, playerBig=None):
        if (not self.collided) and playerBig != None:
            self.collided = True if playerBig else False
        return False

