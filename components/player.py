import pygame as pg
from enum import Enum
from components.spritesheet import *
from components.Tiles.DynamicTile import DynamicTile
from components.Tiles.MysteryBox import MysteryBoxTile
from components.Tiles.Flag import Flag
from components.constants import RESOLUTION
import time


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
        self.player_win = False
        self.walk_speed = 4
        self.run_speed = 30
        self.check_collisions = True

        self.position = pg.math.Vector2(0, 0)
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, self.gravity)
        self.jump_sound = pygame.mixer.Sound('assets/sounds/jump.wav')

        self.frame_count = 0
        self.image = None
        self.rect = pg.Rect(0, 0, 32, 32)
        self.calc_player_image()
        self.rect = pg.Rect(self.position[0], self.position[1], 32, 32 * 2)
        self.jump_cooldown = 0
        self.invincibility = 0
        self.num_lives = 3
        # time mario has been alive
        self.start_time = time.time()

    def draw(self, surface, offset):
        """Method to draw the player to the screen.

        Args:
          surface: the surface to draw the player to.

        Returns:
          None
        """
        surface.blit(self.image, (self.rect.x - offset, self.rect.y))

    def winning_animation(self):
        """
        If the player is not on the ground, make him jump. If he is on the ground, make him walk right
        until he reaches the end of the level
        :return: signal to the main scene that the player has reached the end of the level
        """
        if not self.on_ground:
            self.RUN_KEY = False
            self.acceleration.y = 0
            self.velocity.y = 2.5
            self.velocity.x = 0
            self.LEFT_KEY = False
            self.RIGHT_KEY = False
        else:
            self.check_collisions = False
            self.velocity.y = 0
            self.walk_speed = 1
            self.RIGHT_KEY = True
            self.LEFT_KEY = False
            if self.position.x >= 6400:
                self.RIGHT_KEY = False
                return True
        return False

    def lose_health(self):
        """
        If the player is not invincible, decrease the player's power and set the player's invincibility
        to 90 frames
        """
        if self.invincibility <= 0:
            self.power_decrease()
            self.invincibility = 90
        pass

    def power_decrease(self):
        """
        If the player is on fire, make them big. If they're big, make them small. If they're small, kill
        them
        """
        if self.player_size == Power.FIRE:
            self.player_size = Power.BIG
        elif self.player_size == Power.BIG:
            self.player_size = Power.SMALL
            self.rect = pg.Rect(self.position[0], self.position[1], 32, 32)
        elif self.player_size == Power.SMALL:
            self.player_size = Power.DEAD

    def update(self, dt, tiles, min_x):
        """
        The function updates the player's position, checks for collisions, and calculates the player's
        image

        :param dt: delta time
        :param tiles: A list of all the tiles in the level
        :param min_x: The minimum x value of the screen
        """
        self.frame_count += 1
        self.jump_cooldown -= 1
        self.invincibility -= 1
        self.horizontal_movement(dt, min_x)
        if self.check_collisions == True:
            self.check_collisions_x(tiles)
        self.vertical_movement(dt)
        if self.check_collisions == True:
            self.check_collisions_y(tiles)
        self.calc_player_image()

    def horizontal_movement(self, dt, min_x):
        """
        If the player is not jumping, and the player is moving left or right, the player's state is set
        to running

        :param dt: time since last frame
        :param min_x: The minimum x position the player can move to
        """
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
        """
        If the player is not dead, then the player's velocity is increased by the acceleration
        multiplied by the time. 
        If the player's velocity is greater than 7, then the player's velocity is set to 7. 
        The player's position is then increased by the player's velocity multiplied by the time plus the
        acceleration multiplied by .5 multiplied by the time squared. 
        The player's rect bottom is then set to the player's position. 
        If the player's velocity is less than 0.2 and the player is on the ground, then the player is
        not jumping. 
        If the player's rect bottom is greater than the resolution, then the player is dead

        :param dt: time since last frame
        """
        if not self.player_win:
            self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7:
            self.velocity.y = 7
        self.position.y += self.velocity.y * dt + \
            (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y

        if abs(self.velocity.y) < 0.2 and self.on_ground:
            self.is_jumping = False

        if self.rect.bottom > RESOLUTION[0]:
            self.player_size = Power.DEAD

    def limit_velocity(self, max_vel):
        """
        If the velocity is greater than the max velocity, set it to the max velocity. If the velocity is
        less than the negative max velocity, set it to the negative max velocity. If the velocity is
        between the max and negative max velocities, leave it alone. If the velocity is less than .01,
        set it to 0

        :param max_vel: The maximum velocity the player can move at
        """
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0

    def calc_player_image(self):
        """
        The function is called when the player is in the game and it changes the image of the player
        depending on the state of the player
        """
        if self.player_size == Power.SMALL:
            self.sprites = MARIO_S_SPRITES
        elif self.player_size == Power.BIG:
            self.sprites = MARIO_M_SPRITES
        elif self.player_size == Power.FIRE:
            self.sprites = MARIO_FIRE_SPRITES
        elif self.player_size == Power.DEAD:
            pass

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

    def reset(self):
        """
        The function resets the player's state, size, position, velocity, acceleration, and rect
        """
        self.player_state = State.IDLE
        self.player_size = Power.FIRE
        self.position = pg.math.Vector2(0, 0)
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, self.gravity)
        self.rect = pg.Rect(self.position[0], self.position[1], 32, 32 * 2)

    def jump(self):
        """
        If the player is on the ground and the jump cooldown is less than 0, then the player is jumping,
        the player is jumping, the player's velocity is set to -11, the player is no longer on the
        ground, and the jump cooldown is set to 15
        """
        if self.on_ground and self.jump_cooldown < 0:
            self.player_state = State.JUMPING
            self.jump_sound.play()
            self.is_jumping = True
            self.velocity.y -= 11
            self.on_ground = False
            self.jump_cooldown = 15

    def bounce_off_enemy(self):
        """
        If the player is not jumping, then the player is jumping
        """
        if self.jump_cooldown < 0:
            self.player_state = State.JUMPING
            self.is_jumping = True
            self.velocity.y -= 13
            self.on_ground = False
            self.jump_cooldown = 15

    def get_hits(self, tiles):
        """
        It takes a list of tiles and returns a list of tiles that collide with the player

        :param tiles: A list of rects that the player can collide with
        :return: The hits list is being returned.
        """
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def check_collisions_x(self, tiles):
        """
        If the player is moving right and hits a flag, the player wins. If the player is moving right
        and hits a tile, the player stops moving right. If the player is moving left and hits a tile,
        the player stops moving left

        :param tiles: A list of all the tiles in the level
        :return: The position of the player.
        """
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                if isinstance(tile, Flag):
                    self.player_win = True
                    return
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x

            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    def check_collisions_y(self, tiles):
        """
        If the player is moving down, set the player's position to the top of the tile, and set the
        player's velocity to 0. If the player is moving up, set the player's position to the bottom of
        the tile, and set the player's velocity to 0.

        :param tiles: A list of all the tiles in the game
        """

        if self.check_collisions:
            self.on_ground = False

        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if isinstance(tile, Flag):
                self.player_win = True
                continue
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
                    increaseScore = tile.collide(
                        self.player_size) and isinstance(tile, MysteryBoxTile)
                    self.score += 100 if increaseScore else 0
