import Box2D
import pygame
from components.Enemies.Enemy import EnemySprite, world_to_box_ratio, box_to_world_ratio, HEIGHT
from components.spritesheet import GOOMBA_SPRITE


class Goomba(EnemySprite):
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

        self.image = GOOMBA_SPRITE[0]
        """The current image of the Goomba to be displayed."""

        self.sprite_source = GOOMBA_SPRITE

        self.rect = self.image.get_rect()
        """The hitbox of the Goomba to determine Pybox collisions for game mechanics."""

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
            self.image = self.sprite_source[2]
            self.toRemove = True
            self.count += 1
        elif self.walk_frame == 25:
            self.image_index = (self.image_index + 1) % 2
            self.image = self.sprite_source[self.image_index]
            self.walk_frame = 0
        else:
            self.walk_frame += 1
        return flag
