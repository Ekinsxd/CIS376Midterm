import pygame

# Drawable
# The Tile class is a subclass of the pygame.sprite.Sprite class


class Pipe(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet, scale):
        """
        It takes in an image, x and y coordinates, and a spritesheet, and then it loads the image from
        the spritesheet, scales it to 32x32, and then sets the x and y coordinates to the ones passed in

        :param image: The image to be loaded in
        :param x: The x coordinate of the top left corner of the sprite
        :param y: The y coordinate of the top left corner of the sprite
        :param spritesheet: The spritesheet that the image is on
        :param scale: the scale tuple factor
        """
        pygame.sprite.Sprite.__init__(self)
        if image != None and spritesheet != None:
            self.image = pygame.transform.scale_by(spritesheet[image], scale)

        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        """
        It takes the image and the rect of the sprite and draws it to the surface

        :param surface: The surface to draw the image on
        """
        surface.blit(self.image, (self.rect.x, self.rect.y))
