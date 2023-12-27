import pygame

class Scoreboard:
    """A class to hold scoreboard resources & assets"""

    def __init__(self, snake_game):
        """Initializing the scoreboard attributes"""
        self.screen = snake_game.screen
        self.screen_rect = self.screen.get_rect()

        self.game_font = pygame.font.Font(None, 30)
        self.text_color = (0,0,0)

        self.score = 0

        self.prep_score()

    def prep_score(self):
        """Preps the score"""
        rounded_score = round(self.score, -1)
        score_string = "Score: " + "{:,}".format(rounded_score)
        self.score_img = self.game_font.render(score_string, True, self.text_color)
        self.score_rect = self.score_img.get_rect()
        self.score_rect.top = 10
        self.score_rect.right = self.screen_rect.right - 10


    def draw_score(self):
        """Draws the score on the screen"""
        self.screen.blit(self.score_img, self.score_rect)
        
