import pygame
from components.constants import RESOLUTION, FONT_DIR  # (800, 600)
import time
from components.spritesheet import MARIO_S_SPRITES


# This class is a subclass of the pygame.sprite.Sprite class. It has a constructor that takes a font
# object, a color, and a position. It has a method called update that takes a score and displays it on
# the screen.
class ScoreLabel(pygame.sprite.Sprite):
    def __init__(self):
        """
        It's a function that initializes the class.
        """
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(FONT_DIR, 20)
        self.mario_image = pygame.transform.scale(MARIO_S_SPRITES[0], (24, 24))
        self.clock_image = pygame.transform.scale(
            pygame.image.load('assets/clock.png'), (24, 24))

    def draw(self, surface, score, num_lives, player_time):
        """
        It draws the score, lives, and time to the screen
        
        :param surface: The surface to draw the score on
        :param score: int
        :param num_lives: The number of lives the player has
        :param player_time: the time the player started the game
        """
        delta_time = time.time() - player_time
        # Write score to screen surface
        score_text = str(score).zfill(7)
        lives_text = f' x {num_lives}'
        time_text = "   {:.0f}".format(400 - delta_time)

        score_label = self.font.render(score_text, True, (255, 255, 255))
        lives_label = self.font.render(lives_text, True, (255, 255, 255))
        time_label = self.font.render(time_text, True, (255, 255, 255))

        score_width, _ = self.font.size(score_text)
        lives_width, _ = self.font.size(lives_text)
        time_width, _ = self.font.size(time_text)

        surface.blit(
            self.mario_image, (RESOLUTION[0]*0.01, RESOLUTION[1]*0.04))
        surface.blit(
            lives_label, (RESOLUTION[0]*0.04, RESOLUTION[1]*0.05))
        surface.blit(
            score_label, (RESOLUTION[0]*0.95 - score_width, RESOLUTION[1]*0.05))
        surface.blit(
            time_label, (RESOLUTION[0]*0.95 - time_width - score_width * 1.1, RESOLUTION[1]*0.05))
        surface.blit(
            self.clock_image, (RESOLUTION[0]*0.95 - time_width - score_width * 1.1 + 16, RESOLUTION[1]*0.04))
