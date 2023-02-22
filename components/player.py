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
        self.faceRight = True
        self.calcPlayerImage()
        self.rect = pg.Rect(100, 100, 32, 32)
        self.image = self.sprites[0]
        self.image = pg.transform.scale(self.image, (32, 32))

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
        self.image = pg.transform.scale(self.image, (32, 32 * ratio))

    def getRect(self):
        """Getter method to return the player's rectangle 
        (can be used to access the position).

        Args:
          None

        Returns
          A Sprite.rect object.
        """
        return self.rect

    def setImage(self, color):
        """A setter method to change the apperance of the player.

        Args:
          color: the color to change the Player Object to.

        Returns:
          None
        """
        self.image.fill(color)

    def moveLeft(self):
        """Method to move the player to the left.

        Args:
          None

        Returns:
          None
        """
        self.rect.x -= 3 if self.rect.x - 3 > 0 else 0

    def moveDown(self):
        """Method to move the player down.

        Args:
          None

        Returns:
          None
        """
        self.rect.y += 3

    def moveUp(self):
        """Method to move the player up.

        Args:
          None

        Returns:
          None
        """
        self.rect.y -= 3 if self.rect.y - 3 > 0 else 0

    def moveRight(self):
        """Method to move the player to the right.

        Args:
          None

        Returns:
          None
        """
        self.rect.x += 3

    def update(self):
        """Method that is not used, but declared because of inheriting the Sprite class."""
        pass
