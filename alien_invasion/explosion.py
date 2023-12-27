import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """Class to handle the explosion animations"""

    def __init__(self, ai_game, center, size):
        """Initialise the attributes & assets"""
        super().__init__()
        self.screen = ai_game.screen

        self.images = []
        
        for num in range(1,6):
            img = pygame.image.load(f"images/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20,20))
            if size == 2:
                img = pygame.transform.scale(img, (50,50))
            if size == 3:
                img = pygame.transform.scale(img, (160,160))
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = center

        # Setting a timer of 100ms
        self.last_frame = pygame.time.get_ticks()
        self.delay = 75

    def update(self):
        """Updates the index of the image list to animate the explosion"""
        self.current_frame = pygame.time.get_ticks()

        if self.index < len(self.images) - 1:
            if self.current_frame - self.last_frame > self.delay: # using a nested if statement to set timer
                self.last_frame = self.current_frame
                self.index += 1
                self.image = self.images[self.index]
        else:
            self.kill() # we don't need to reset the self.index to 0 again since we use the kill() sprite function here & since in the init fn we have set the self.index as 0
    
    def draw(self):
        """Draws the explosion on the screen"""
        self.screen.blit(self.image, self.rect)    


