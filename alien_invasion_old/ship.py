import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """ A class to manage the ship """

    def __init__(self, ai_game): # 2 parameters: self reference & reference to instance of Alien invasion class
        """ Initialise the ship & set its starting position """
        super().__init__()
        self.screen = ai_game.screen # assign the screen of Alien invasion class to an attribute of Ship, so we can access it easily in all the methods in this class
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() # we access the screen’s rect attribute using the get_rect() method and assign it to self.screen_rect. Doing so allows us to place the ship in the correct location on the screen

        # Load the ship & get its rectangle
        self.image = pygame.image.load('images/ship1.bmp') # loading the image by calling pygame.image.load() & give location of ship image
        self.rect = self.image.get_rect() # getting rectangle of the image.

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom # Matching the ships rect midbottom to the screen's rect midbottom

        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        # movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the ship's position on the basis of the movement flag """
        # Update the ship's x value & not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update rect object from self.x
        self.rect.x = self.x
        
    def blitme(self):
        """ Draw the ship at its current location """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)