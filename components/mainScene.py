import pygame as pg
import sys
from pygame.locals import *
import components.constants as constants
import components.spritesheet as spritesheet
from components.Tiles.TileMap import TileMap
from components.player import Player, Power
from components.Enemies.Koopa import Koopa
from components.Enemies.Goomba import Goomba
from components.ScoreLabel import ScoreLabel
from components.Background.backgroundMap import BackgroundMap
import Box2D
from time import sleep


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
        self.bg = BackgroundMap(
            'assets/mario_world.csv', spritesheet.BACKGROUND_SPRITES)
        self.scoreLabel = ScoreLabel()
        self.x_offset = 0
        self.gameOver = False
        self.backgroundSprites = pg.sprite.Group()
        self.winner_animation = False
        self.main_music = pg.mixer.Sound('assets/sounds/music.wav')
        self.win_music = pg.mixer.Sound('assets/sounds/win.wav')
        self.lose_music = pg.mixer.Sound('assets/sounds/game_over.wav')

    def run(self):
        """A method that contains the main game loop.

        Args:
          None

        Returns:
          None
        """
        self.main_music.play()
        # Test Enemies implementation
        koopa_group = pg.sprite.Group()
        wall_group = self.map.dynamicGroup
        goomba1 = Goomba(540, 180, Display.world)
        goomba_group = pg.sprite.Group()
        goomba_group.add(goomba1)
        koopa_spawn = [4300]
        goomba_spawn = [800, 900, 1500, 1550, 1600, 2000,
                        2100, 2800, 2900, 3000, 4350, 4400, 4400, 4450]

        while not self.gameOver:  # main game loop
            # Gets and deals with events.
            dt = self.clock.tick(
                constants.FRAME_LIMIT) * .001 * 60

            for player in self.players:
                current_x = player.rect.x

                for k_x in koopa_spawn:
                    if current_x >= k_x:
                        koopa_spawn.remove(k_x)
                        koopa_group.add(
                            Koopa(current_x + 410, 180, Display.world))

                for g_x in goomba_spawn:
                    if current_x >= g_x:
                        goomba_spawn.remove(g_x)
                        goomba_group.add(
                            Goomba(current_x + 410, 180, Display.world))

                if not player.player_win:
                    for event in pg.event.get():
                        # ignore input if won.
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_a:
                                player.LEFT_KEY = True
                            elif event.key == pg.K_d:
                                player.RIGHT_KEY = True
                            elif event.key == pg.K_w:
                                player.jump()
                            elif event.key == pg.K_LSHIFT:
                                player.RUN_KEY = True

                        if event.type == pg.KEYUP:
                            if event.key == pg.K_a:
                                player.LEFT_KEY = False
                            elif event.key == pg.K_d:
                                player.RIGHT_KEY = False
                            elif event.key == pg.K_w:
                                if player.is_jumping:
                                    player.velocity.y *= .25
                            elif event.key == pg.K_LSHIFT:
                                player.RUN_KEY = False

                        if event.type == QUIT:
                            pg.quit()
                            sys.exit()

                else:
                    if self.win_music.get_num_channels() == 0:
                        self.win_music.play()
                    self.main_music.stop()
                    self.winner_animation = True
                    if player.winning_animation():
                        self.gameOver = True
                        player.sprite_index = 0
                        # not working?

                        while self.win_music.get_num_channels() != 0:
                            pass
                        self.winGame()

                if player.rect.x > self.x_offset + constants.RESOLUTION[0] / 2 and \
                        self.x_offset < player.position.x:
                    self.x_offset = player.position.x - \
                        constants.RESOLUTION[0] / 2

                if not self.gameOver:
                    # Update Box2D Physics
                    Display.world.Step(Display.time_step,
                                       Display.vel_iters, Display.pos_iters)
                    player.update(dt, self.map.tiles, self.x_offset)

                    self.canvas.fill(constants.SKY_BLUE)
                    self.bg.load_map()
                    self.map.load_map()

                    koopa_group.update(wall_group, self.players)
                    goomba_group.update(wall_group, koopa_group, self.players)

                    # draw map, enemies, then player
                    self.bg.draw_map(self.canvas, (-self.x_offset, 0))
                    self.map.draw_map(self.canvas, (-self.x_offset, 0))

                    # ENEMIES
                    for koopa in koopa_group:
                        if koopa.update(wall_group, self.players):
                            player.bounce_off_enemy()
                        koopa.draw(self.canvas, self.x_offset)
                    for goomba in goomba_group:
                        if goomba.update(wall_group, koopa_group, self.players):
                            player.bounce_off_enemy()
                        goomba.draw(self.canvas, self.x_offset)

                    player.draw(self.canvas, self.x_offset)
                    self.scoreLabel.draw(
                        self.canvas, player.score, player.num_lives, player.start_time)
            if not self.gameOver:
                self.screen.blit(self.canvas, (0, 0))
                pg.display.update()

            if player.num_lives <= 0:
                self.endGame()
            elif player.player_size == Power.DEAD:
                self.x_offset = 0
                player.num_lives -= 1
                player.reset()

        while self.gameOver:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
            self.screen.blit(self.canvas, (0, 0))
            pg.display.update()

    def endGame(self):
        """
        It takes the canvas, fills it with black, creates a font, creates a label, gets the width and
        height of the label, and then blits the label to the canvas
        """
        self.canvas.fill(constants.BLACK)
        font = pg.font.Font(constants.FONT_DIR, 20)
        gameover_label = font.render("GAME OVER", True, (255, 255, 255))
        width, height = font.size("GAME OVER")
        self.canvas.blit(
            gameover_label, (constants.RESOLUTION[0]*0.5 - width/2, constants.RESOLUTION[1]*0.5 - height/2))
        self.gameOver = True
        self.main_music.stop()
        self.lose_music.play()

    def winGame(self):
        """
        It takes the canvas, fills it with black, creates a font, creates a label, gets the width and
        height of the label, and then blits the label to the canvas
        """
        self.canvas.fill(constants.BLACK)
        font = pg.font.Font(constants.FONT_DIR, 20)
        gameover_label = font.render("You Win!", True, (255, 255, 255))
        width, height = font.size("You Win!")
        self.canvas.blit(
            gameover_label, (constants.RESOLUTION[0]*0.5 - width/2, constants.RESOLUTION[1]*0.5 - height/2))
        self.gameOver = True
