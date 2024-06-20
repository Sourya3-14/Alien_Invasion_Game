import pygame
from pygame.sprite import Sprite

class Life(Sprite):
    """A class to manage the Lifes left image"""

    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.path = ai_game.path
    
        #Loading the heart image
        self.image = pygame.image.load(self.path+"/Images/Heart.png")
        self.rect = self.image.get_rect()