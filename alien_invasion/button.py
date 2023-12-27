import pygame

class Button():
    """Class for button behaviour"""

    def __init__(self, ai_game, msg):
        """Initialise button resources"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions & the properties of the button
        self.width, self.height = 120, 50
        self.text_color =  (0,0,0) # white
        self.button_color = (255,255,255) # black
        self.font = pygame.font.SysFont(None, 38)

        # Build the rect & center it
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The message needs to prepped only once
        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        """Prep the message"""
        self.msg_img = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_img, self.msg_img_rect)
       