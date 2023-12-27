import pygame.font
from pygame.sprite import Group

from ship import Ship

class ScoreBoard():
    """Class to hold scoreboard attributes & methods"""

    def __init__(self, ai_game):
        """Initialize the scoreboard resources"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #Font settings for scoring info
        self.text_color = (255,255,255) # white
        self.bg_color = (0,0,0) #black
        self.font = pygame.font.SysFont(None, 25)
        #self.button_color = self.settings.bg_color

        self._prep_score()
        self._prep_high_score()
        self.prep_level()
        self.prep_ships()

    def _prep_score(self):
        """Preps the message"""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: " + "{:,}".format(rounded_score) # str means string in this variable
        #self.score_img = self.font.render(score_str,True,self.text_color,self.settings.bg_color) # or we could initialise the button_color & pass that as a argument here instead of self.settings.bg_color
        self.score_img = self.font.render(score_str,True,self.text_color,self.bg_color)

        # Display the score at the top right edge of the screen
        self.score_rect = self.score_img.get_rect()
        self.score_rect.top = 20
        self.score_rect.right = self.screen_rect.right - 20

    def check_high_score(self):
        """Check to see if there is a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self._prep_high_score()

    
    def _prep_high_score(self):
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: " + "{:,}".format(rounded_high_score)
        self.high_score_img = self.font.render(high_score_str,True,self.text_color,self.bg_color)

        # Get the rect & position the high score img
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = "Level: " + str(self.stats.level)
        self.level_img = self.font.render(level_str, True, self.text_color, self.bg_color)

        # Get the rect & position it
        self.level_rect = self.level_img.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * (ship.rect.width + 10)
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        "Draw the scores on the screen"
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_img, self.level_rect)
        self.ships.draw(self.screen)
