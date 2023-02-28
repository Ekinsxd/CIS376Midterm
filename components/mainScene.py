import pygame as pg
import sys
from pygame import key
from pygame.locals import *
import components.constants as constants
import components.spritesheet as spritesheet
from components.tiles import *
from components.player import Player
from components.Enemies import Koopa, Goomba


class Display:
    """An object usedß to create a display for the player to see the program/game."""
    # Create Box2D world
    gravity = Box2D.b2Vec2(0, -35.0)
    world = Box2D.b2World(gravity, doSleep=False)
    time_step = 1.0/60
    vel_iters, pos_iters = 6, 2

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
        # Test Enemies implementation
        koopa = Koopa(1400, 180, Display.world)
        koopa_group = pg.sprite.Group()
        koopa_group.add(koopa)
        wall_group = pg.sprite.Group()
        goomba1 = Goomba(1000, 180, Display.world)
        goomba_group = pg.sprite.Group()
        goomba_group.add(goomba1)

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
                        elif event.key == pygame.K_LSHIFT:
                            player.RUN_KEY = False

                    if event.type == QUIT:
                        pg.quit()
                        sys.exit()
                if player.rect.x > self.x_offset + constants.RESOLUTION[0] / 2 and \
                        self.x_offset < player.position.x:
                    self.x_offset = player.position.x - \
                        constants.RESOLUTION[0] / 2

                # Update Box2D Physics
                Display.world.Step(Display.time_step,
                                   Display.vel_iters, Display.pos_iters)
                player.update(dt, self.map.tiles, self.x_offset)

                self.canvas.fill((0, 180, 240))
                self.map.load_map()
                koopa_group.update(wall_group, self.players)
                goomba_group.update(wall_group, koopa_group, self.players)
                # draw map, enemies, then player
                self.map.draw_map(self.canvas, (-self.x_offset, 0))
                for koopa in koopa_group:
                    if koopa.update(wall_group, self.players):
                        player.bounce_off_enemy()
                    koopa.draw(self.canvas, self.x_offset)
                for goomba in goomba_group:
                    if goomba.update(wall_group, koopa_group, self.players):
                        player.bounce_off_enemy()
                    goomba.draw(self.canvas, self.x_offset)

                player.draw(self.canvas, self.x_offset)
                # print(player.position)

            self.screen.blit(self.canvas, (0, 0))
            pg.display.update()
