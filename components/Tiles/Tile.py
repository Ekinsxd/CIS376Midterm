import pygame

# Drawable
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        if image != None and spritesheet != None:
            self.image = pygame.transform.scale(spritesheet[image], (32, 32))
            
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))



