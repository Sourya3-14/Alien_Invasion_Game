import pygame.font
from pygame.sprite import Group

from life import Life

class Scoreboard:
    """A class to report scoring information"""
    def __init__(self,ai_game):
        """Initialize scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoreboard information
        self.text_colour = (255,255,255)
        self.font1 = pygame.font.SysFont('showcard gothic',30)# for high score
        self.font = pygame.font.SysFont('showcard gothic',20)# for score and level

        # Preapare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image"""
        roundded_score = round(self.stats.score,2)
        score_str = "{:,}".format(roundded_score)
        self.score_image = self.font.render(score_str,True,self.text_colour,self.settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        high_score = round(self.stats.high_score,2)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font1.render(high_score_str,True,self.text_colour,self.settings.bg_color)
        self.HIGH_SCORE = self.font.render("HIGHEST SCORE",True,self.text_colour,self.settings.bg_color)

        # Display the high score at the top of the screen
        self.HIGH_SCORE_rect = self.HIGH_SCORE.get_rect()
        self.HIGH_SCORE_rect.centerx = self.screen_rect.centerx
        self.HIGH_SCORE_rect.y = 10 
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.y = self.HIGH_SCORE_rect.bottom + 10

    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render("Level "+level_str,True,self.text_colour,self.settings.bg_color)

        #Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range (self.stats.ships_left ):
            ship = Life(self.ai_game)
            ship.rect.x = 10 + ship_number * (ship.rect.width + 10)
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw score, level and ships to the screen"""
        self.screen.blit(self.HIGH_SCORE,self.HIGH_SCORE_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there is an new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            with open("high_score.txt","r+") as f:
                f.write(str(self.stats.high_score))