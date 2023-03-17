import Box2D
import pygame
from components.Enemies.Enemy import EnemySprite, world_to_box_ratio, box_to_world_ratio, HEIGHT
from components.spritesheet import KOOPA_SPRITE


class Koopa(EnemySprite):
    """A Turtle that is an enemy to the Player. 
    If a Koopa touches the player when the player is not in the air, the player dies or takes damage.
    If the player jumps on top of the Koopa, the Koopa hides in its shell.
    The the player jumps on top of the shell, the shell will move and terminate any Goombas or other Koopas."""

    def __init__(self, x, y, world):
        """Creates a Koopa at a location.
        Params:
            x: the x coordinate position for the Goomba in PIXEL Position. Left decreases X val, Right increases X value.
            y: the y coordinate position for the Goomba in PIXEL Position. UP increases Y val, DOWN decreases Y val.

        Returns:
            None
        """
        super().__init__()

        self.body = world.CreateDynamicBody(
            position=(x * world_to_box_ratio, (y) * world_to_box_ratio))
        """The Box2D for the Goomba, used to calcuate the position of the body based on physics."""

        shape = Box2D.b2PolygonShape(
            box=(12 * world_to_box_ratio, 20 * world_to_box_ratio))
        fixDef = Box2D.b2FixtureDef(
            shape=shape, friction=0.5, restitution=0, density=1)
        fixDef.filter.groupIndex = -1

        # self.physics_box = self.body.CreateFixture(fixDef)
        """For the Box2D physics collision box."""

        self.dirty = 2

        self.image = KOOPA_SPRITE[0]
        """The current image of the Koopa to be displayed."""

        self.rect = self.image.get_rect()
        # time.sleep(1)
        """The hitbox of the Goomba to determine Pybox collisions for game mechanics."""

        self.sprite_source = KOOPA_SPRITE

        self.isInShell = False
        """If the Koopa is in its shell from being stepped on by the player."""
        self.isMovingShell = False
        """State if the shell is moving from the Player jumping on the Koopa shell."""

        self.shell_direction = 2
        """Helps with the shell's velocity. when the shell is moving."""
        self.killable_count = 0
        self.time_before_kick = 0

    def draw(self, surface, offset):
        surface.blit(self.image, (self.rect.x - offset, self.rect.y))

    def update(self, wallGroup, players):
        """
        Updates the location and state of the Koopa.

        Params:
        None

        Returns:
        True if the Koopa collided with the player
        """
        flag = False
        self.rect.center = self.body.position[0] * \
            box_to_world_ratio, HEIGHT - \
            self.body.position[1] * box_to_world_ratio

        collided = pygame.sprite.spritecollide(self, wallGroup, False)
        player_collision = pygame.sprite.spritecollide(self, players, False)
        if len(player_collision) > 0:
            for player in players:
                if (player.is_jumping and not player.on_ground) and not self.isInShell:
                    self.time_before_kick = pygame.time.get_ticks()
                    player.invincibility = 10
                    self.hideInShell()
                    flag = True
                elif (player.is_jumping or not player.on_ground) and self.isInShell and pygame.time.get_ticks() - self.time_before_kick >= 10:
                    player.invincibility = 10
                    self.time_before_kick = pygame.time.get_ticks()
                    force = -1
                    if self.rect.collidepoint(player.rect.bottomright):
                        force *= -1
                    self.kickedInShell(force)
                    flag = True
                else:
                    player.lose_health()
                    flag = True

        if len(collided) > 0:
            # time.sleep(1)
            self.changeDirection()

        if not self.isDead and not self.isInShell:
            self.body.linearVelocity = Box2D.b2Vec2(
                self.shell_direction / 2, 0)
            self.image = pygame.transform.flip(self.image, False, True)

        if self.count == 5:
            self.body.DestroyFixture(self.physics_box)
            self.kill()
        elif self.isDead:
            self.toRemove = True
            self.count += 1
        elif self.walk_frame == 25 and not self.isInShell:
            self.image_index = (self.image_index + 1) % 2
            self.image = KOOPA_SPRITE[self.image_index]
            if self.shell_direction > 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.walk_frame = 0
        elif not self.isInShell:
            self.walk_frame += 1
        else:
            self.image = KOOPA_SPRITE[2]
            self.body.linearVelocity = Box2D.b2Vec2(self.shell_direction, 0)

        return flag

    def hideInShell(self):
        """
        Causes the Koopa to hide in its shell due to the Player jumping on top of it.

        Params:
        None

        Returns:
        None
        """
        self.isInShell = True
        self.stomp_sound.play()
        self.image = KOOPA_SPRITE[2]

    def kickedInShell(self, force):
        """
        Causes the Koopa to move in a certain direction due to the Player jumping on it during
        it's inShell State.

        @Params:
        force: Helps determine where the shell should move. force should be a val to determine
        where the player is facing. Left should be negative, Right should be positive.

        Returns:
        None
        """
        if not self.isMovingShell:
            self.shell_direction = 2

            if force < 0:
                self.shell_direction *= -1
        else:
            self.shell_direction = 0

        self.isMovingShell = not self.isMovingShell

    def changeDirection(self):
        self.shell_direction *= -1
