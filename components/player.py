import pygame as pg
from components.constants import RESOLUTION
from enum import Enum
from components.spritesheet import *


class Power(Enum):
    """An enum to represent the size of the player."""
    SMALL = 0
    BIG = 1
    BIG_STAR = 2
    FIRE = 3
    FIRE_STAR = 4


class State(Enum):
    """An enum to represent the size of the player."""
    IDLE = 0
    RUNNING = 1
    JUMPING = 2


class Player(pg.sprite.Sprite):
    """An object that represents the player which the user controls."""

    def __init__(self):
        """Constructor to create the Player Object."""
        super().__init__()
        self.playerState = State.IDLE
        self.playerSize = Power.SMALL
        self.sprites = []
        self.LEFT_KEY, self.RIGHT_KEY, self.RUN_KEY, self.FACING_LEFT = False, False, False, False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .35, -.22
        self.walk_speed = 4
        self.run_speed = 10

        self.position = pg.math.Vector2(0, 0)
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, self.gravity)

        self.image = None
        self.rect = pg.Rect(0, 0, 32, 32)
        self.calcPlayerImage()

    def draw(self, surface, offset):
        """Method to draw the player to the screen.

        Args:
          surface: the surface to draw the player to.

        Returns:
          None
        """
        surface.blit(self.image, (self.rect.x - offset, self.rect.y))

    def update(self, dt, tiles, min_x):
        self.horizontal_movement(dt, min_x)
        self.checkCollisionsx(tiles)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles)

    def horizontal_movement(self, dt, min_x):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= self.run_speed if self.RUN_KEY else self.walk_speed
        elif self.RIGHT_KEY:
            self.acceleration.x += self.run_speed if self.RUN_KEY else self.walk_speed
        elif self.on_ground and self.velocity.x != 0:
            if abs(self.velocity.x) < 0.3:
                self.velocity.x = 0
                self.acceleration.x = 0
            else:
                self.acceleration.x += self.friction if self.velocity.x > 0 else -self.friction
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        add_pos = self.velocity.x * dt + \
            (self.acceleration.x * .5) * (dt * dt)
        if self.position.x + add_pos > min_x:
            self.position.x += add_pos
            self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7:
            self.velocity.y = 7
        self.position.y += self.velocity.y * dt + \
            (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0

    def calcPlayerImage(self):
        ratio = 1
        if self.playerSize == Power.SMALL:
            self.sprites = MARIO_S_SPRITE
        elif self.playerSize == Power.BIG:
            self.sprites = MARIO_M_SPRITE
            ratio = 2
        elif self.playerSize == Power.FIRE:
            self.sprites = MARIO_FIRE_SPRITE
            ratio = 2

        self.image = self.sprites[0]
        self.rect = pg.Rect(self.position[0], self.position[1], 32, 32 * ratio)
        self.image = pg.transform.scale(self.image, (32, 32 * ratio))

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 13
            self.on_ground = False

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisionsx(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    def checkCollisionsy(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:  # Hit tile from the top
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:  # Hit tile from the bottom
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y
