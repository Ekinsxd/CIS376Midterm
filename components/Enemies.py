#!/usr/bin/env python
# Make sure the local python is anaconda and that the pybox2d environment is activated
import Box2D
import pygame
import spritesheet
import time
import constants
#################
#We will need these in the Engine
world_to_box_ratio = 1/100
box_to_world_ratio = 100
gravity = Box2D.b2Vec2(0.5, -10.0)
world = Box2D.b2World(gravity=gravity, doSleep=False)

WIDTH = constants.RESOLUTION[0]
HEIGHT = constants.RESOLUTION[1]
pygame.init()
canvas = pygame.Surface((WIDTH, HEIGHT))
window = pygame.display.set_mode((800, 600))
#Set fps
clock = pygame.time.Clock()
black = (0, 0, 0)
#############################################

my_spritesheet = spritesheet.Spritesheet("../assets/Super Mario Bros Sprite", "gif")
GOOMBA_SPRITE = [
    my_spritesheet.parse_sprite('g3'),
    my_spritesheet.parse_sprite('g2'),
    my_spritesheet.parse_sprite('g1'),        
                 ]

KOOPA_SPRITE = [
                my_spritesheet.parse_sprite('k3'),
                my_spritesheet.parse_sprite('k4'),
                my_spritesheet.parse_sprite('k1'),
                my_spritesheet.parse_sprite('k2'),
                my_spritesheet.parse_sprite('k5'),
                my_spritesheet.parse_sprite('k6'),
                ]
############

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

class Goomba(pygame.sprite.Sprite):
    """A mushroom that is an enemy to the Player. 
    If a Goomba touches the player when the player is not in the air, the player dies or takes damage.
    If the player jumps on top of the Goomba, the Goomba dies."""

    def __init__(self, x, y):
        """Creates a Goomba at a location.
        Params:
            x: the x coordinate position for the Goomba in PIXEL Position. Left decreases X val, Right increases X value.
            y: the y coordinate position for the Goomba in PIXEL Position. UP increases Y val, DOWN decreases Y val.

        Returns:
            None
        """
        super().__init__()
        
        self.body = world.CreateDynamicBody(position=(x *world_to_box_ratio, (y) * world_to_box_ratio))
        """The Box2D for the Goomba, used to calcuate the position of the body based on physics."""
        
        shape = Box2D.b2PolygonShape(box=(13 * world_to_box_ratio, 14 * world_to_box_ratio))
        fixDef = Box2D.b2FixtureDef(shape=shape, friction=0.1, restitution=0, density = 0.5)
        fixDef.filter.groupIndex = -1
        
        self.physics_box = self.body.CreateFixture(fixDef)
        """For the Box2D physics collision box."""
        
        self.dirty = 2
        
        self.image = GOOMBA_SPRITE[0]
        """The current image of the Goomba to be displayed."""
        
        self.rect = self.image.get_rect()
        print(self.rect)
        #time.sleep(1)
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
        self.body.linearVelocity = Box2D.b2Vec2(-1,0)
        self.previous_position = self.body.position
        
    def update(self):
        """Updates the location and state of the Goomba."""
        self.rect.center = self.body.position[0] * box_to_world_ratio, HEIGHT - self.body.position[1] * box_to_world_ratio
        print('box2d x:', self.body.position[0])
        print('box2d y:',self.body.position[1])
        print(self.rect.centerx)
        print(HEIGHT - self.rect.centery)
        collided = pygame.sprite.spritecollide(self, wallGroup, False)

        if len(collided) > 0:
            print('collision OCCURRED')
            #time.sleep(1)
            self.changeDirection()
        if not self.isDead:
            if self.move_left:
                    #self.body.ApplyForce(Box2D.b2Vec2(-0.1, 0), self.body.position, True)
                self.body.linearVelocity = Box2D.b2Vec2(-1,0)
            else:
                #self.body.ApplyForce(Box2D.b2Vec2(0.1, 0), self.body.position, True)
                self.body.linearVelocity = Box2D.b2Vec2(1,0)

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
    
    def terminate(self):
        self.isDead = True
    
    def changeDirection(self):
        self.move_left = not self.move_left

class Koopa(pygame.sprite.Sprite):
    """A Turtle that is an enemy to the Player. 
    If a Koopa touches the player when the player is not in the air, the player dies or takes damage.
    If the player jumps on top of the Koopa, the Koopa hides in its shell.
    The the player jumps on top of the shell, the shell will move and terminate any Goombas or other Koopas."""

    def __init__(self, x, y):
        """Creates a Koopa at a location.
        Params:
            x: the x coordinate position for the Goomba in PIXEL Position. Left decreases X val, Right increases X value.
            y: the y coordinate position for the Goomba in PIXEL Position. UP increases Y val, DOWN decreases Y val.

        Returns:
            None
        """
        super().__init__()
        
        self.body = world.CreateDynamicBody(position=(x *world_to_box_ratio, (y) * world_to_box_ratio))
        """The Box2D for the Goomba, used to calcuate the position of the body based on physics."""
        
        shape = Box2D.b2PolygonShape(box=(14 * world_to_box_ratio, 20 * world_to_box_ratio))
        fixDef = Box2D.b2FixtureDef(shape=shape, friction=0.1, restitution=0, density = 0.5)
        fixDef.filter.groupIndex = -1
        
        self.physics_box = self.body.CreateFixture(fixDef)
        """For the Box2D physics collision box."""
        
        self.dirty = 2
        
        self.image = KOOPA_SPRITE[0]
        """The current image of the Koopa to be displayed."""
        
        self.rect = self.image.get_rect()
        print(self.rect)
        #time.sleep(1)
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
        """Helps determine where the GKoopa should move."""
        self.body.linearVelocity = Box2D.b2Vec2(-1,0)

        self.isInShell = False
        self.isMovingShell = False
        self.shell_direction = 2
        
    def update(self):
        """Updates the location and state of the Goomba."""
        self.rect.center = self.body.position[0] * box_to_world_ratio, HEIGHT - self.body.position[1] * box_to_world_ratio
        print('box2d x:', self.body.position[0])
        print('box2d y:',self.body.position[1])
        print(self.rect.centerx)
        print(HEIGHT - self.rect.centery)
        collided = pygame.sprite.spritecollide(self, wallGroup, False)

        if len(collided) > 0:
            print('collision OCCURRED')
            #time.sleep(1)
            self.changeDirection()
        if not self.isDead:
            if self.move_left:
                    #self.body.ApplyForce(Box2D.b2Vec2(-0.1, 0), self.body.position, True)
                self.body.linearVelocity = Box2D.b2Vec2(-1,0)
            else:
                #self.body.ApplyForce(Box2D.b2Vec2(0.1, 0), self.body.position, True)
                self.body.linearVelocity = Box2D.b2Vec2(1,0)
                
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
            self.body.linearVelocity = Box2D.b2Vec2(self.shell_direction,0)
        else:
            self.image = KOOPA_SPRITE[2]
            self.body.linearVelocity = Box2D.b2Vec2(0,0)
    
    def terminate(self):
        self.isDead = True
    
    def hideInShell(self):
        self.isInShell = True
    
    def kickedInShell(self, force):
        if force < 0:
            self.shell_direction = -2
        self.isMovingShell = True
    
    def changeDirection(self):
        self.move_left = not self.move_left


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




