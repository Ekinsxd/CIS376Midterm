#!/usr/bin/python
import sys
import pygame
import csv
import os
import Box2D
import components.mainScene as mainScene
sys.path.append("../")

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spritesheet[image], (32, 32))
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        ##Added Box2D physics.
        self.body = mainScene.Display.world.CreateStaticBody(
            position=(x/100, (600 -32 - y) / 100),
            shapes = Box2D.b2PolygonShape(box=(0.32,0.32))
            )

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 32
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface, camera):
        surface.blit(self.map_surface, camera)

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    tiles.append(Tile('mbox', x * self.tile_size,
                                 y * self.tile_size, self.spritesheet))

                elif tile == '20':
                    tiles.append(Tile('ground', x * self.tile_size,
                                 y * self.tile_size, self.spritesheet))
                elif tile == '30':
                    tiles.append(Tile('brick', x * self.tile_size,
                                 y * self.tile_size, self.spritesheet))
                elif tile == '25':
                    tiles.append(Tile('box', x * self.tile_size,
                                 y * self.tile_size, self.spritesheet))
                    # Move to next tile in current row
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
