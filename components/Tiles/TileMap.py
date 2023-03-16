import pygame
import csv
import os
from components.Tiles.BrickTile import BrickTile
from components.Tiles.StaticTile import StaticTile
from components.Tiles.MysteryBox import MysteryBoxTile
from components.Tiles.Flag import Flag


class TileMap():
    def __init__(self, filename, spritesheet):
        """
        It creates a surface, sets the colorkey to black, and then loads the map.
        
        :param filename: The name of the file that contains the map data
        :param spritesheet: The spritesheet that contains the tiles
        """
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
        """
        It takes the map surface and blits it to the camera.
        
        :param surface: The surface to draw the map on
        :param camera: A pygame.Rect object that represents the camera's position and size
        """
        surface.blit(self.map_surface, camera)

    def load_map(self):
        """
        It draws the map to the screen
        """
        self.dynamicGroup.update(self.tiles)
        self.dynamicGroup.draw(self.map_surface)
        self.staticGroup.draw(self.map_surface)

    # Only called for initial start of game

    def read_csv(self, filename):
        """
        It reads a csv file and returns a list of lists
        
        :param filename: the name of the file to be read
        :return: A list of lists.
        """
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    # Only called for initial start of game

    def load_tiles(self, filename):
        """
        It reads a csv file and creates a list of tiles based on the values in the csv file
        
        :param filename: The name of the file to load the map from
        :return: The tiles are being returned.
        """
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
                    self.staticGroup.add(boxTile)

                elif tile == '2':  # FLAG
                    flag = Flag('flag', x * self.tile_size,
                                y * self.tile_size, self.spritesheet)
                    tiles.append(flag)
                    self.staticGroup.add(flag)

                elif tile == '34': #PIPE
                    pipeTile = StaticTile('pipe', x * self.tile_size,
                                         y * self.tile_size, self.spritesheet)
                    tiles.append(pipeTile)
                    self.staticGroup.add(pipeTile)

                # Move to next tile in current row
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
