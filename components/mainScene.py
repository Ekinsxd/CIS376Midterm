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

    def run(self):
        """A method that contains the main game loop.

        Args:
          None

        Returns:
          None
        """

        while True:  # main game loop

            # Gets and deals with events.

            self.clock.tick(constants.FRAME_LIMIT)
            pg.display.update()

            for event in pg.event.get():
                try:                    # press space to iterate the automata maze
                    if event.type == KEYDOWN:
                        # quit if escape is pressed
                        if event.key == K_ESCAPE:
                            pg.quit()
                            sys.exit()
                except Exception as e:
                    print(e)

                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

            keys = key.get_pressed()
            for player in self.players:
                if keys[K_w]:
                    player.moveUp()
                if keys[K_a]:
                    player.moveLeft()
                if keys[K_s]:
                    player.moveDown()
                if keys[K_d]:
                    player.moveRight()

            self.canvas.fill((0, 180, 240))
            self.map.load_map()
            self.map.draw_map(self.canvas, (0, 0))

            self.screen.blit(self.canvas, (0, 0))
            self.players.draw(self.screen)
            pg.display.update()
