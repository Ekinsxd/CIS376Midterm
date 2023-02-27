import pygame
import json
import sys
sys.path.append('../')

# Source: https://github.com/ChristianD37/YoutubeTutorials/tree/master/spritesheet


class Spritesheet:
    """This class helps us animate Mario and other enemies without having to have multiple images."""

    def __init__(self, filename, filetype):
        self.filename = filename + "." + filetype
        self.sprite_sheet = pygame.image.load(self.filename).convert()
        self.meta_data = filename + ".json"

        with open(self.meta_data) as file:
            self.data = json.load(file)

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image = self.get_sprite(x, y, w, h)
        return image


#####################################################################
pygame.init()
canvas = pygame.Surface((800, 600))
window = pygame.display.set_mode((800, 600))
black = (0, 0, 0)


my_spritesheet = Spritesheet("assets/Super Mario Bros Sprite", "gif")

MARIO_M_SPRITES = [
    my_spritesheet.parse_sprite('lm1'),  # jump
    my_spritesheet.parse_sprite('lm7'),  # idle
    my_spritesheet.parse_sprite('lm6'),  # duck
    my_spritesheet.parse_sprite('lm3'),
    my_spritesheet.parse_sprite('lm4'),
    my_spritesheet.parse_sprite('lm5'),
    my_spritesheet.parse_sprite('lm4'),
]

MARIO_S_SPRITES = [
    my_spritesheet.parse_sprite('sm7'),  # idle
    my_spritesheet.parse_sprite('sm2'),  # jump
    my_spritesheet.parse_sprite('sm7'),  # idle is duck
    my_spritesheet.parse_sprite('sm4'),
    my_spritesheet.parse_sprite('sm5'),
    my_spritesheet.parse_sprite('sm6'),
    my_spritesheet.parse_sprite('sm5'),
]

MARIO_FIRE_SPRITES = [
    my_spritesheet.parse_sprite('fm7'),  # idle
    my_spritesheet.parse_sprite('fm1'),  # jump
    my_spritesheet.parse_sprite('fm6'),  # duck
    my_spritesheet.parse_sprite('fm3'),
    my_spritesheet.parse_sprite('fm4'),
    my_spritesheet.parse_sprite('fm5'),
    my_spritesheet.parse_sprite('fm4'),
]

my_spritesheet = Spritesheet(
    "assets/Super Mario Bros Sprite", "gif")
GOOMBA_SPRITE = [
    my_spritesheet.parse_sprite('g3'),
    my_spritesheet.parse_sprite('g2'),
    my_spritesheet.parse_sprite('g1'),
]

KOOPA_SPRITE = [
    my_spritesheet.parse_sprite('k3'),
    my_spritesheet.parse_sprite('k4'),
    my_spritesheet.parse_sprite('k1'),
    my_spritesheet.parse_sprite('k2'),
    my_spritesheet.parse_sprite('k5'),
    my_spritesheet.parse_sprite('k6'),
]
# my_spritesheet2 = Spritesheet("assets/items-objects", "png")
# sprite7 = [
#     my_spritesheet2.parse_sprite('m1'),
#     my_spritesheet2.parse_sprite('m2'),
#     my_spritesheet2.parse_sprite('flower'),
#     my_spritesheet2.parse_sprite('box'),
#     my_spritesheet2.parse_sprite('coin'),
#     my_spritesheet2.parse_sprite('fire'),
# ]

tile_sheet = Spritesheet("assets/generalSpriteSheet", "gif")
TILE_SPRITES = {
    "brick": tile_sheet.parse_sprite('brick'),
    "ground": tile_sheet.parse_sprite('ground'),
    "box": tile_sheet.parse_sprite('box'),
    "mbox": tile_sheet.parse_sprite('mbox'),
    "coin": tile_sheet.parse_sprite('coin'),
    "pipe": tile_sheet.parse_sprite('pipe'),
    "flag": tile_sheet.parse_sprite('flag')
}
# running = True
# i = 0
# print(i + 1)
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 i += 1

#     canvas.fill((255, 255, 255))
#     canvas.blit(MARIO_M_SPRITES[i % len(MARIO_M_SPRITES)], (32, 32))
#     window.blit(canvas, (0, 0))
#     pygame.display.update()

# pygame.quit()
