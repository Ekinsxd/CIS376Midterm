import Box2D
import pygame
import components.constants as constants
world_to_box_ratio = 1/100
box_to_world_ratio = 100
gravity = Box2D.b2Vec2(0, -30.0)

WIDTH = constants.RESOLUTION[0]
HEIGHT = constants.RESOLUTION[1]


class EnemySprite(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image_index = 0
        """What image to get for self.image."""

        self.isDead = False
        """Helps determine when to display a different sprite."""

        self.toRemove = False
        """Helps to determine if to remove enemy."""

        self.count = 0
        """Helps to determine when to remove after being dead."""

        self.walk_frame = 0
        """Helps to determine when to change the image of the enemy."""

        self.move_left = True
        """Helps determine where to move."""

        self.stomp_sound = pygame.mixer.Sound('assets/sounds/stomp.wav')

        self.dirty = 2

    def terminate(self):
        """
        Kills this enemy.

        Params:
        None

        Returns:
        None

        """
        if not self.isDead:
            self.isDead = True
            self.stomp_sound.play()
        self.image = self.sprite_source[2]

    def changeDirection(self):
        """
        Changes direction, this is a helper method to help with collision with a wall.

        Params:
        None

        Returns:
        None

        """
        self.move_left = not self.move_left
