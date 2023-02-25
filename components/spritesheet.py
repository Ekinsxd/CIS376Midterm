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
#pygame.init()
#canvas = pygame.Surface((800, 600))
#window = pygame.display.set_mode((800, 600))
#black = (0, 0, 0)

"""
my_spritesheet = Spritesheet("../assets/Super Mario Bros Sprite", "gif")
MARIO_M_SPRITE = [my_spritesheet.parse_sprite('lm1'),
                  my_spritesheet.parse_sprite('lm2'),
                  my_spritesheet.parse_sprite('lm3'),
                  my_spritesheet.parse_sprite('lm4'),
                  my_spritesheet.parse_sprite('lm5'),
                  my_spritesheet.parse_sprite('lm6'),
                  my_spritesheet.parse_sprite('lm7'),
                  my_spritesheet.parse_sprite('lm8'),
                  my_spritesheet.parse_sprite('lm9'),
                  my_spritesheet.parse_sprite('lm10'),
                  my_spritesheet.parse_sprite('lm11'),
                  my_spritesheet.parse_sprite('lm12'),
                  my_spritesheet.parse_sprite('lm13'),
                  my_spritesheet.parse_sprite('lm14'),
                  ]
MARIO_S_SPRITE = [
    my_spritesheet.parse_sprite('sm1'),
    my_spritesheet.parse_sprite('sm2'),
    my_spritesheet.parse_sprite('sm3'),
    my_spritesheet.parse_sprite('sm4'),
    my_spritesheet.parse_sprite('sm5'),
    my_spritesheet.parse_sprite('sm6'),
    my_spritesheet.parse_sprite('sm7'),
    my_spritesheet.parse_sprite('sm8'),
    my_spritesheet.parse_sprite('sm9'),
    my_spritesheet.parse_sprite('sm10'),
    my_spritesheet.parse_sprite('sm11'),
    my_spritesheet.parse_sprite('sm12'),
    my_spritesheet.parse_sprite('sm13'),
]

MARIO_ICON_SPRITE = [my_spritesheet.parse_sprite('tm1'),
                     my_spritesheet.parse_sprite('tm2')]

MARIO_FIRE_SPRITE = [my_spritesheet.parse_sprite('fm1'),
                     my_spritesheet.parse_sprite('fm2'),
                     my_spritesheet.parse_sprite('fm3'),
                     my_spritesheet.parse_sprite('fm4'),
                     my_spritesheet.parse_sprite('fm5'),
                     my_spritesheet.parse_sprite('fm6'),
                     my_spritesheet.parse_sprite('fm7'),
                     my_spritesheet.parse_sprite('fm8'),
                     my_spritesheet.parse_sprite('fm9'),
                     my_spritesheet.parse_sprite('fm10'),
                     my_spritesheet.parse_sprite('fm11'),
                     my_spritesheet.parse_sprite('fm12'),
                     my_spritesheet.parse_sprite('fm13'),
                     my_spritesheet.parse_sprite('fm14'),
                     ]

GOOMBA_SPRITE = [my_spritesheet.parse_sprite('g1'),
                 my_spritesheet.parse_sprite('g2'),
                 my_spritesheet.parse_sprite('g3'),
                 ]

KOOPA_SPRITE = [my_spritesheet.parse_sprite('k1'),
                my_spritesheet.parse_sprite('k2'),
                my_spritesheet.parse_sprite('k3'),
                my_spritesheet.parse_sprite('k4'),
                my_spritesheet.parse_sprite('k5'),
                my_spritesheet.parse_sprite('k6'),

                ]
my_spritesheet2 = Spritesheet("../assets/items-objects", "png")
sprite7 = [
    my_spritesheet2.parse_sprite('m1'),
    my_spritesheet2.parse_sprite('m2'),
    my_spritesheet2.parse_sprite('flower'),
    my_spritesheet2.parse_sprite('box'),
    my_spritesheet2.parse_sprite('coin'),
    my_spritesheet2.parse_sprite('fire'),
]

tile_sheet = Spritesheet("../assets/generalSpriteSheet", "gif")
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
# length = len(sprite7)
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
#     canvas.blit(pygame.transform.scale(
#         TILE_SPRITES[i % len(TILE_SPRITES)], (32, 32)), (0, 600 - 100))
#     window.blit(canvas, (0, 0))
#     pygame.display.update()

# pygame.quit()
"""
