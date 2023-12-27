import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to hold ship image & position"""

    def __init__(self, ai_game, health):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Set the health variables
        self.hp_start = health
        self.hp_remaining = health
        self.red = (255,0,0)
        self.green = (0,255,0)

        # Load the ship image & get its rect
        self.image = pygame.image.load("images/ship2.bmp")
        self.rect = self.image.get_rect()

        # Position the ship at the bottom center
        self.rect.center = self.screen_rect.center
        self.rect.bottom = self.screen_rect.height - 100

        # Setting the exact location of the ship
        self.x = int(self.rect.x)
        self.y = int(self.rect.y)

        # Setting the movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    # Update ship position
    def update(self):
        """Moves the ship position within the game window"""
        if self.moving_right and self.rect.right <= self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left >= 0:
            self.x -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom + 20  <= self.screen_rect.bottom: # adding 15 to account for the healthbar doesn't get hidden when moving playing down
            self.y += self.settings.ship_speed
        if self.moving_up and self.rect.top >= 0:
            self.y -= self.settings.ship_speed

        # Reset self.x to self.rect.x because rect doesnt take floats  & same for y  
        self.rect.x = self.x
        self.rect.y = self.y

    def center_me(self):
        """Reset the ship to its original location"""
        self.rect.center = self.screen_rect.center
        self.rect.bottom = self.screen_rect.height - 100
        # Reset the pos of x & y
        self.x = self.rect.x
        self.y = self.rect.y

    # Draw the ship
    def draw(self):
        self.screen.blit(self.image, self.rect)
        
        # Draw the health bar
        pygame.draw.rect(self.screen, self.red, (self.rect.x, self.rect.bottom + 5, self.rect.width, 7))
        
        pygame.draw.rect(self.screen, self.green, (self.rect.x, self.rect.bottom + 5, int(self.rect.width * (self.hp_remaining/ self.hp_start)), 7))