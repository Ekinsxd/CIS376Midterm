import pygame as pg
import sys
from pygame import key
from pygame.locals import *
import components.constants as constants
import components.spritesheet as spritesheet
from components.tiles import *
from components.player import Player


class Display:
    """An object usedß to create a display for the player to see the program/game."""

    def __init__(self):
        """Constructor to create the display/screen"""
        pg.init()
        pg.display.set_caption('Mar.io')

        self.resolution = constants.RESOLUTION
        """Resolution of the screen"""
        self.canvas = pg.Surface(constants.RESOLUTION)
        self.screen = pg.display.set_mode(self.resolution)
        self.clock = pg.time.Clock()
        self.fps = constants.FRAME_LIMIT
        self.players = pg.sprite.Group()
        self.players.add(Player())
        self.map = TileMap('assets/mario_world.csv', spritesheet.TILE_SPRITES)
        self.x_offset = 0

    def run(self):
        """A method that contains the main game loop.

        Args:
          None

        Returns:
          None
        """

        while True:  # main game loop

            # Gets and deals with events.
            dt = self.clock.tick(
                constants.FRAME_LIMIT) * .001 * 60

            for player in self.players:
                for event in pg.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            player.LEFT_KEY = True
                        elif event.key == pygame.K_d:
                            player.RIGHT_KEY = True
                        elif event.key == pygame.K_w:
                            player.jump()
                        elif event.key == pygame.K_LSHIFT:
                            player.RUN_KEY = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            player.LEFT_KEY = False
                        elif event.key == pygame.K_d:
                            player.RIGHT_KEY = False
                        elif event.key == pygame.K_w:
                            if player.is_jumping:
                                player.velocity.y *= .25
                                player.is_jumping = False
                        elif event.key == pygame.K_LSHIFT:
                            player.RUN_KEY = False

                    if event.type == QUIT:
                        pg.quit()
                        sys.exit()
                if player.rect.x > self.x_offset + constants.RESOLUTION[0] / 2 and \
                        self.x_offset < player.position.x:
                    self.x_offset = player.position.x - \
                        constants.RESOLUTION[0] / 2

                player.update(dt, self.map.tiles, self.x_offset)
                self.canvas.fill((0, 180, 240))
                self.map.load_map()
                self.map.draw_map(self.canvas, (-self.x_offset, 0))
                player.draw(self.canvas, self.x_offset)
                print(player.position)

            self.screen.blit(self.canvas, (0, 0))
            pg.display.update()
