import pygame
from components.constants import RESOLUTION #(800, 600)

class ScoreLabel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font('assets/Press_Start_2P/PressStart2P-Regular.ttf', 20)
        
    def draw(self, score, surface):
        # Write score to screen surface
        scoreText = f'Score: {score}'
        label = self.font.render(scoreText, True, (255, 255, 255))
        width, _ = self.font.size(scoreText)
        surface.blit(label, (RESOLUTION[0]*0.5-(width*0.5), RESOLUTION[1]*0.08))