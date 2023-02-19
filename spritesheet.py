import pygame

class Spritesheet:
    """This class helps us animate Mario and other enemies without having to have multiple images."""

    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface( (w,h) )
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0, 0), (x,y,w,h))
        return sprite

pygame.init()
canvas = pygame.Surface( (800,600) )
window = pygame.display.set_mode( (800, 600) )

my_spritesheet = Spritesheet("Super Mario Bros Sprite.gif")
sprite1 = my_spritesheet.get_sprite(0,0, 32, 64)

running = True
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    canvas.fill((255, 255, 255))
    canvas.blit(sprite1, (0, 600 - 64))
    window.blit(canvas, (0,0))
    pygame.display.update()

