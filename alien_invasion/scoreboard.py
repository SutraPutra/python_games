import pygame.font
from pygame.sprite import Group
from ship import Ship
from ship_life import ShipLife

class ScoreBoard():
    """Class to manage scoreboard object"""
    def __init__(self, ai_game):
        """Initialize the scoreboard assets & resources"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (255,255,255) # white
        self.font = pygame.font.SysFont(None, 25)

        self._prep_score()
        self._prep_high_score()
        self.prep_level()
        self.prep_ships()

    def _prep_score(self):
        """Preps the score"""
        # Render the score
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: " + "{:,}".format(rounded_score)
        self.score_img = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Get the rect & position it to top-right corner
        self.score_rect = self.score_img.get_rect()
        self.score_rect.top = 20
        self.score_rect.left = 15 # setting the score to the left edge of the screen


    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self._prep_high_score()

    def _prep_high_score(self):
        """Preps the high score"""
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: " + "{:,}".format(rounded_high_score)
        self.high_score_img = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Get the rect & position it
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20


    def prep_level(self):
        """Preps the level img"""
        level_str = "Level: " + str(self.stats.level)
        self.level_img = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Get the rect & position it below the score
        self.level_rect = self.level_img.get_rect()
        self.level_rect.left = self.score_rect.left
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group() # creating the pygame Sprite Group
        for ship_number in range(self.stats.ship_left):
            ship_life = ShipLife(self.ai_game)
            ship_life.rect.x = self.screen_rect.width - 35 - (ship_number * ship_life.rect.width + 10)
            ship_life.rect.y = 20
            self.ships.add(ship_life)


    def draw_score(self):
        """Draws the scoreboard on the screen"""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.level_img, self.level_rect)   
        self.screen.blit(self.high_score_img, self.high_score_rect)  
        self.ships.draw(self.screen)