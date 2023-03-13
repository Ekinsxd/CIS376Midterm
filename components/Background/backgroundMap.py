import pygame
import csv
import os
from components.Background.background import Background


# > This class is used to create a background map for the game
class BackgroundMap():
    def __init__(self, filename, spritesheet):
        """
        It loads the background images from the spritesheet, then loads the map from the file.
        
        :param filename: The name of the file that contains the map data
        :param spritesheet: The spritesheet that contains the tiles
        """
        self.spriteGroup = pygame.sprite.Group()
        self.tile_size = 32
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.bg_images = self.load_bg(filename)
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
        It takes the background images and draws them to the map surface.
        """
        self.spriteGroup.update(self.bg_images)
        self.spriteGroup.draw(self.map_surface)

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

    def load_bg(self, filename):
        """
        It reads a csv file and creates a list of background objects
        
        :param filename: The name of the CSV file to load
        :return: The tiles are being returned.
        """
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '13':
                    image = Background('hillB', x * self.tile_size,
                                       y * self.tile_size, self.spritesheet, 2.5)
                    tiles.append(image)
                    self.spriteGroup.add(image)
                if tile == '14':
                    image = Background('hillS', x * self.tile_size,
                                       y * self.tile_size, self.spritesheet, 2)
                    tiles.append(image)
                    self.spriteGroup.add(image)
                elif tile == '27':
                    image = Background('cloudS', x * self.tile_size,
                                       y * self.tile_size, self.spritesheet, 2)
                    tiles.append(image)
                    self.spriteGroup.add(image)
                elif tile == '22':
                    image = Background('cloudM', x * self.tile_size,
                                       y * self.tile_size, self.spritesheet, 3)
                    tiles.append(image)
                    self.spriteGroup.add(image)
                elif tile == '3':
                    image = Background('bushS', x * self.tile_size,
                                       y * self.tile_size, self.spritesheet, 2)
                    tiles.append(image)
                    self.spriteGroup.add(image)
                elif tile == '1':
                    image = Background('castle', x * self.tile_size,
                                       y * self.tile_size, self.spritesheet, 3)
                    tiles.append(image)
                    self.spriteGroup.add(image)

                    # Move to next tile in current row
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
