#!/usr/bin/env python
# Make sure the local python is anaconda and that the pybox2d environment is activated
import Box2D
import pygame
from components.spritesheet import *
import components.spritesheet as spritesheet
import time
import components.constants as constants
import sys
sys.path.append('../')
#################
# We will need these in the Engine
world_to_box_ratio = 1/100
box_to_world_ratio = 100
gravity = Box2D.b2Vec2(0.5, -10.0)
#world = Box2D.b2World(gravity=gravity, doSleep=False)

WIDTH = constants.RESOLUTION[0]
HEIGHT = constants.RESOLUTION[1]


class Goomba(pygame.sprite.Sprite):
    """A mushroom that is an enemy to the Player. 
    If a Goomba touches the player when the player is not in the air, the player dies or takes damage.
    If the player jumps on top of the Goomba, the Goomba dies."""

    def __init__(self, x, y, world):
        """Creates a Goomba at a location.
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
            box=(13 * world_to_box_ratio, 14 * world_to_box_ratio))
        fixDef = Box2D.b2FixtureDef(
            shape=shape, friction=0.1, restitution=0, density=0.5)
        fixDef.filter.groupIndex = -1

        self.physics_box = self.body.CreateFixture(fixDef)
        """For the Box2D physics collision box."""

        self.dirty = 2

        self.image = GOOMBA_SPRITE[0]
        """The current image of the Goomba to be displayed."""

        self.rect = self.image.get_rect()
        # time.sleep(1)
        """The hitbox of the Goomba to determine Pybox collisions for game mechanics."""

        self.image_index = 0
        """What image to get for self.image."""

        self.isDead = False
        """Helps determine when to display a different sprite."""

        self.toRemove = False
        """Helps to determine when to remove the Goomba."""

        self.count = 0
        """Helps to determine when to remove this Goomba after being dead."""

        self.walk_frame = 0
        """Helps to determine when to change the image of the Goomba."""

        self.move_left = True
        """Helps determine where the Goomba should move."""

        # Inital movement of Goomba.
        self.body.linearVelocity = Box2D.b2Vec2(-1, 0)

    def draw(self, surface, offset):
        surface.blit(self.image, (self.rect.x - offset, self.rect.y))

    def update(self, wallGroup, koopa, players):
        """
        Updates the location and state of the Goomba.

        Params:
        None

        Returns:
        None
        """
        flag = False
        self.rect.center = self.body.position[0] * \
            box_to_world_ratio, HEIGHT - \
            self.body.position[1] * box_to_world_ratio
        collided = pygame.sprite.spritecollide(self, wallGroup, False)
        koopa_collided = pygame.sprite.spritecollide(self, koopa, False)
        player_collided = pygame.sprite.spritecollide(self, players, False)

        if len(player_collided) > 0:
            for player in player_collided:
                if player.is_jumping or not player.on_ground:
                    self.terminate()
                    flag = True
                else:
                    player.lose_health()

        if len(collided) > 0:
            # time.sleep(1)
            self.changeDirection()
        if len(koopa_collided) != 0:
            if koopa_collided[0].isMovingShell:
                self.terminate()

        if not self.isDead:
            if self.move_left:
                self.body.linearVelocity = Box2D.b2Vec2(-1, 0)
            else:
                self.body.linearVelocity = Box2D.b2Vec2(1, 0)

        if self.count == 5:
            self.body.DestroyFixture(self.physics_box)
            self.kill()
        elif self.isDead:
            self.image = GOOMBA_SPRITE[2]
            self.toRemove = True
            self.count += 1
        elif self.walk_frame == 25:
            self.image_index = (self.image_index + 1) % 2
            self.image = GOOMBA_SPRITE[self.image_index]
            self.walk_frame = 0
        else:
            self.walk_frame += 1
        return flag

    def terminate(self):
        """
        This causes the Goomba to get squished, and will remove the Goomba
        from game eventually.

        Params:
        None

        Returns:
        None

        """
        self.isDead = True
        self.image = GOOMBA_SPRITE[2]

    def changeDirection(self):
        """
        Changes direction of Goomba, this is a helper method to help with collision with a wall.

        Params:
        None

        Returns:
        None

        """
        self.move_left = not self.move_left


class Koopa(pygame.sprite.Sprite):
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
            shape=shape, friction=0.1, restitution=0, density=0.5)
        fixDef.filter.groupIndex = -1

        self.physics_box = self.body.CreateFixture(fixDef)
        """For the Box2D physics collision box."""

        self.dirty = 2

        self.image = KOOPA_SPRITE[0]
        """The current image of the Koopa to be displayed."""

        self.rect = self.image.get_rect()
        # time.sleep(1)
        """The hitbox of the Goomba to determine Pybox collisions for game mechanics."""

        self.image_index = 0
        """What image to get for self.image."""

        self.isDead = False
        """Helps determine when to display a different sprite."""

        self.toRemove = False
        """Helps to determine when to remove the Koopa."""

        self.count = 0
        """Helps to determine when to remove this Koopa after being dead."""

        self.walk_frame = 0
        """Helps to determine when to change the image of the Koopa."""

        self.move_left = True
        """Helps determine where the Koopa should move."""
        self.body.linearVelocity = Box2D.b2Vec2(-1, 0)

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
                if (player.is_jumping or not player.on_ground) and not self.isInShell:
                    self.hideInShell()
                    self.time_before_kick = pygame.time.get_ticks()
                    flag = True
                elif (player.is_jumping or not player.on_ground) and self.isInShell and pygame.time.get_ticks() - self.time_before_kick >= 100:
                    force = 1
                    if player.LEFT_KEY:
                        force *= -1
                    self.kickedInShell(force)
                    flag = True
                else:
                    player.lose_health()

        if len(collided) > 0:
            # time.sleep(1)
            self.changeDirection()

        if not self.isDead:
            if self.move_left:
                #self.body.ApplyForce(Box2D.b2Vec2(-0.1, 0), self.body.position, True)
                self.body.linearVelocity = Box2D.b2Vec2(-1, 0)
            else:
                #self.body.ApplyForce(Box2D.b2Vec2(0.1, 0), self.body.position, True)
                self.body.linearVelocity = Box2D.b2Vec2(1, 0)

        if self.count == 5:
            self.body.DestroyFixture(self.physics_box)
            self.kill()
        elif self.isDead:
            self.toRemove = True
            self.count += 1
        elif self.walk_frame == 25 and not self.isInShell:
            self.image_index = (self.image_index + 1) % 2
            self.image = KOOPA_SPRITE[self.image_index]
            self.walk_frame = 0
        elif not self.isInShell:
            self.walk_frame += 1
        elif self.isInShell and self.isMovingShell:
            self.body.linearVelocity = Box2D.b2Vec2(self.shell_direction, 0)
        else:
            self.image = KOOPA_SPRITE[2]
            self.body.linearVelocity = Box2D.b2Vec2(0, 0)
        return flag

    def terminate(self):
        """
        Terminates the Koopa right away. This should be used when the player casts a fireball.

        Params:
        None

        Returns:
        None
        """
        self.isDead = True

    def hideInShell(self):
        """
        Causes the Koopa to hide in its shell due to the Player jumping on top of it.

        Params:
        None

        Returns:
        None
        """
        self.isInShell = True
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
        if force < 0:
            self.shell_direction *= -1
        self.isMovingShell = True

    def changeDirection(self):
        self.shell_direction *= -1
        self.body.linearVelocity = Box2D.b2Vec2(self.shell_direction, 0)


""" Below is a self-contained test.
class Ground(pygame.sprite.Sprite):
    def __init__(self, x,y,w,h):
        super().__init__()
        self.body = world.CreateStaticBody(position=(x,y), shapes=Box2D.b2PolygonShape(box=(w,h)))
        self.image = pygame.Surface((2*w*box_to_world_ratio, 2 * h * box_to_world_ratio))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * box_to_world_ratio, HEIGHT - self.body.position.y * box_to_world_ratio
    
    def update():
        pass

class Wall(pygame.sprite.Sprite):
    def __init__(self, x,y,w,h):
        super().__init__()
        self.body = world.CreateStaticBody(position=(x,y), shapes=Box2D.b2PolygonShape(box=(w,h)))
        self.image = pygame.Surface((2*w*box_to_world_ratio, 2 * h * box_to_world_ratio))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * box_to_world_ratio, HEIGHT - self.body.position.y * box_to_world_ratio




ground = Ground(0, 1, 25, 1)
groundGroup = pygame.sprite.Group()
wall1 = Ground(0, 6, 0.5, 6)
wall2 = Ground(8, 6, 0.5, 6)
wallGroup = pygame.sprite.Group()
wallGroup.add(wall1)
wallGroup.add(wall2)
groundGroup.add(ground)
goomba = Goomba(400, 220)
goomba1 = Goomba(200, 240)
goomba_group = pygame.sprite.Group()
goomba_group.add(goomba)
goomba_group.add(goomba1)
koopa = Koopa(600, 200)
koopa_group = pygame.sprite.Group()
koopa_group.add(koopa)
running = True

timeStep = 1.0 / 60
vel_iters, pos_iters = 3, 1
while running:
    #time.sleep(1)
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
             running = False
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                goomba.terminate()
                koopa.hideInShell()
                #koopa.terminate()
            if event.key == pygame.K_UP:
                goomba.changeDirection()
                koopa.kickedInShell(1)

    world.Step(timeStep, vel_iters, pos_iters)
    groundGroup.draw(canvas)
    canvas.fill((255, 255, 255))
    wallGroup.draw(canvas)
    goomba_group.update()
    koopa_group.update()
    koopa_group.draw(canvas)
    goomba_group.draw(canvas)
    groundGroup.draw(canvas)
    pygame.display.update()
    window.blit(canvas, (0, 0))
    clock.tick(60)

pygame.quit()
"""
