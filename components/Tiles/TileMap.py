import pygame
import csv
import os
from components.Tiles.BrickTile import BrickTile
from components.Tiles.StaticTile import StaticTile
from components.Tiles.MysteryBox import MysteryBoxTile


class TileMap():
    def __init__(self, filename, spritesheet):
        self.dynamicGroup = pygame.sprite.Group()
        self.staticGroup = pygame.sprite.Group()
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
        self.dynamicGroup.update()
        self.dynamicGroup.draw(self.map_surface)
        self.staticGroup.draw(self.map_surface)

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
                    mysteryTile = MysteryBoxTile('mbox', x * self.tile_size,
                                 y * self.tile_size, self.spritesheet)
                    tiles.append(mysteryTile)
                    self.dynamicGroup.add(mysteryTile)

                elif tile == '20':
                    groundTile = StaticTile('ground', x * self.tile_size,
                                 y * self.tile_size, self.spritesheet)
                    tiles.append(groundTile)
                    self.staticGroup.add(groundTile)
                elif tile == '30':
                    brickTile = BrickTile('brick', x * self.tile_size,
                                 y * self.tile_size, self.spritesheet)
                    tiles.append(brickTile)
                    self.dynamicGroup.add(brickTile)
                elif tile == '25':
                    boxTile = StaticTile('box', x * self.tile_size,
                                 y * self.tile_size, self.spritesheet)
                    tiles.append(boxTile)
                    self.staticGroup.add(brickTile)

                    # Move to next tile in current row
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles