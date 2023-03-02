import pygame as pg
from enum import Enum
from components.spritesheet import *
from components.Tiles.DynamicTile import DynamicTile
from components.Tiles.MysteryBox import MysteryBoxTile


class Power(Enum):
    """An enum to represent the size of the player."""
    DEAD = -1
    SMALL = 0
    BIG = 1
    FIRE = 2


class State(Enum):
    """An enum to represent the size of the player."""
    IDLE = 0
    RUNNING = 1
    JUMPING = 2
    DUCKING = 2


class Player(pg.sprite.Sprite):
    """An object that represents the player which the user controls."""

    def __init__(self):
        """Constructor to create the Player Object."""
        super().__init__()
        self.player_state = State.IDLE
        self.player_size = Power.FIRE
        self.score = 0
        self.sprites = []
        self.LEFT_KEY, self.RIGHT_KEY, self.RUN_KEY, self.FACING_RIGHT = False, False, False, True
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .35, -.22
        self.walk_speed = 4
        self.run_speed = 10

        self.position = pg.math.Vector2(0, 0)
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, self.gravity)

        self.frame_count = 0
        self.image = None
        self.rect = pg.Rect(0, 0, 32, 32)
        self.calc_player_image()
        self.rect = pg.Rect(self.position[0], self.position[1], 32, 32 * 2)
        self.jump_cooldown = 0
        self.invincibility = 0

    def draw(self, surface, offset):
        """Method to draw the player to the screen.

        Args:
          surface: the surface to draw the player to.

        Returns:
          None
        """
        surface.blit(self.image, (self.rect.x - offset, self.rect.y))

    def lose_health(self):
        if self.invincibility <= 0:
            self.power_decrease()
            self.invincibility = 90
        pass

    def power_decrease(self):
        if self.player_size == Power.FIRE:
            self.player_size = Power.BIG
        elif self.player_size == Power.BIG:
            self.player_size = Power.SMALL
            self.rect = pg.Rect(self.position[0], self.position[1], 32, 32)
        elif self.player_size == Power.SMALL:
            self.player_size = Power.DEAD

    def update(self, dt, tiles, min_x):
        self.frame_count += 1
        self.jump_cooldown -= 1
        self.invincibility -= 1
        self.horizontal_movement(dt, min_x)
        self.check_collisions_x(tiles)
        self.vertical_movement(dt)
        self.check_collisions_y(tiles)
        self.calc_player_image()

    def horizontal_movement(self, dt, min_x):
        self.acceleration.x = 0
        if not self.is_jumping:
            self.player_state = State.IDLE
        if self.LEFT_KEY and self.RIGHT_KEY:
            pass
        elif self.LEFT_KEY:
            self.acceleration.x -= self.run_speed if self.RUN_KEY else self.walk_speed

            if not self.is_jumping:
                self.player_state = State.RUNNING
            self.FACING_RIGHT = False
        elif self.RIGHT_KEY:
            self.acceleration.x += self.run_speed if self.RUN_KEY else self.walk_speed

            if not self.is_jumping:
                self.player_state = State.RUNNING
            self.FACING_RIGHT = True
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

        if abs(self.velocity.y) < 0.2 and self.on_ground:
            self.is_jumping = False

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0

    # my_spritesheet.parse_sprite('fm7'),  # idle
    # my_spritesheet.parse_sprite('fm1'),  # jump
    # my_spritesheet.parse_sprite('fm6'),  # duck
    # my_spritesheet.parse_sprite('fm3'),
    # my_spritesheet.parse_sprite('fm4'),
    # my_spritesheet.parse_sprite('fm5'),
    # my_spritesheet.parse_sprite('fm4'),
    def calc_player_image(self):
        ratio = 1
        if self.player_size == Power.SMALL:
            self.sprites = MARIO_S_SPRITES
        elif self.player_size == Power.BIG:
            self.sprites = MARIO_M_SPRITES
            ratio = 2
        elif self.player_size == Power.FIRE:
            self.sprites = MARIO_FIRE_SPRITES
            ratio = 2

        if self.player_state == State.IDLE:
            self.image = self.sprites[0]
        elif self.player_state == State.JUMPING:
            self.image = self.sprites[1]
        elif self.player_state == State.DUCKING:
            self.image = self.sprites[2]
        elif self.player_state == State.RUNNING:
            self.image = self.sprites[3 + (self.frame_count // 10) % 4]

        if self.FACING_RIGHT:
            self.image = pg.transform.flip(self.image, True, False)

        # self.rect = pg.Rect(self.position[0], self.position[1], 32, 32 * ratio)

    def jump(self):
        if self.on_ground and self.jump_cooldown < 0:
            self.player_state = State.JUMPING
            self.is_jumping = True
            self.velocity.y -= 13
            self.on_ground = False
            self.jump_cooldown = 15

    def bounce_off_enemy(self):
        if self.jump_cooldown < 0:
            self.player_state = State.JUMPING
            self.is_jumping = True
            self.velocity.y -= 13
            self.on_ground = False
            self.jump_cooldown = 15

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def check_collisions_x(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    def check_collisions_y(self, tiles):
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
                if isinstance(tile, DynamicTile):
                    increaseScore = tile.collide(self.player_size) and isinstance(tile, MysteryBoxTile)
                    self.score += 100 if increaseScore else 0