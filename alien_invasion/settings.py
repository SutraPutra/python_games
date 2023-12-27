import pygame, math

class Settings():
    """A class to hold all the game settings"""

    def __init__(self, ai_game):
        """Initialise the game settings"""

        # Game window settings
        self.width = 600
        self.height = 800
        self.bg_color = (0,0,0) # not required since we set a bg_img

        # Setting a background image
        self.bg_img = pygame.image.load('images/sky5.jpg')
        self.bg_rect = self.bg_img.get_rect()
        #self.bg_img = pygame.transform.scale(self.bg_img, (self.width,self.height))
        self.tiles = math.ceil(self.height / self.bg_rect.height) + 1
        self.scroll = 0

        # Ship settings
        self.ship_limit = 3 # No. of lives of player
        # Moved another setting to dynamic settings

        # Bullet settings
        self.bullet_width = 5 # defaultl is 5
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)

        # Alien settings
        self.fleet_drop = 15 #default is 15
        self.alien_bullet_color = (255, 255, 255)
        
        self.speed_scaleup = 1.2
        self.initialize_dynamic_settings() # Initialise dynamic settings
        


    def initialize_dynamic_settings(self):
        """Initialise the dynamic settings which change during the game"""
        self.alien_speed = 0.25 # default is 0.25
        self.ship_speed = 1.2
        self.bullet_speed = 2
        self.fleet_direction = 1
        self.alien_hit_points = 100

    def increase_speed(self):
        """Increase the speed of the game"""
        self.alien_speed *= self.speed_scaleup
        self.ship_speed *= self.speed_scaleup
        self.bullet_speed *= self.speed_scaleup
        self.alien_hit_points = int(self.alien_hit_points * self.speed_scaleup)

        