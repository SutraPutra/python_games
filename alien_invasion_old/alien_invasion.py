import sys # Using sys module to exit the game when player quits
import pygame
from time import sleep

from settings import Settings # import Class Settings from module settings.py
from game_stats import GameStats
from scoreboard import ScoreBoard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button


class AlienInvasion():
    """ Overall class to manage game assets & behavior """

    def __init__(self):
        """ Initialise game & create game resources """
        pygame.init() # initialise pygame
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) # set size of the game window
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion") # set title of game window

        self.stats = GameStats(self)
        self.sb = ScoreBoard(self) # Scoreboard object
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() # creating a pygame sprite group for the attribute bullets
        self.aliens = pygame.sprite.Group() # creating a pygame sprite group for alien enemy ships
        self._create_fleet()

        # Make the play button
        self.play_button = Button(self, "Play")

        # Load the game sounds
        pygame.mixer.init()
        self.bullet_fire_sound = pygame.mixer.Sound("./sounds/bullet_fire_sound2.wav")
        self.bullet_fire_sound.set_volume(0.4)
        self.alien_explode_sound = pygame.mixer.Sound("./sounds/alien_explode_sound.wav")
        self.level_up_sound = pygame.mixer.Sound("./sounds/level_up_sound.wav")
        self.ready_go_sound = pygame.mixer.Sound("sounds/ready_go_sound.mp3")
        
        # Settings up the background music, setting volume & looping for infinity.
        pygame.mixer.music.load("./sounds/arcade_theme_track.ogg")
        pygame.mixer.music.set_volume(0.5) # takes values b/w 0 & 1.
        pygame.mixer.music.play(loops=-1)
    
        # Load background image
        # self.bg = pygame.image.load("./images/bg.png")

    def run_game(self):
        """ Start the main loop for the game """
        while True:
            # self.settings.clock.tick(self.settings.fps)

            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_aliens()
            
            self._update_screen()

    # To draw a background image 
    # def draw_bg(self):
    #     """Draw the background image to the game window"""
    #     self.screen.blit(self.bg, (0,0))


    def _check_events(self):
        """ Respond to key presses & mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If the user hits the red x button then
                sys.exit()                # pygame window will close
  
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)        

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)   

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()
            

    def _start_game(self):
        """Reset the stats, removes aliens & bullets, creates a new fleet & centers the ship & hides the cursor"""
        self.settings.initialize_dynamic_settings() # Reset the game settings
        self.stats.reset_stats() # Reset the game statistics
        self.sb._prep_score() # makes the score reset to zero at the start of the game since reset_stats is called
        self.sb.prep_level()
        self.sb.prep_ships()
        self.stats.game_active = True

        # Get rid of any remaining aliens & bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create new fleet & center the ship
        self._create_fleet()
        self.ship.center_ship()                    

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Play the ready go sound when game starts
        self.ready_go_sound.play()


    def _check_keydown_events(self, event):
        """ Responds to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q: # press the 'q' key to exit the game when in full screen
            sys.exit()
        elif event.key == pygame.K_SPACE: # press spacebar to shoot
            self._fire_bullet()
        elif event.key == pygame.K_p: # press P button to hit the play button & start game
            self._start_game()

    def _check_keyup_events(self, event):
        """ Respond to keypresses """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Creates a new bullet and adds it to the bullet group"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self) # creates a instance of the Class Bullet
            self.bullets.add(new_bullet) # adds the bullet to the group (sprite)
            self.bullet_fire_sound.play()

    def _update_bullet(self):
        """Updates the position of bullet and gets rid of old bullets"""
        # Updates the bullet position
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet) 

        self._check_bullet_alien_collisions()
        

    def _check_bullet_alien_collisions(self):
        """Responds to bullet-alien collisions"""
        # Remove any bullets or aliens that collide
        # Check if the bullet has hit any alien, if so, delete the bullet & alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # If collision returns True then increase the score
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens) # multiply by the length since the value is a list in the dictionary collision
            self.sb._prep_score()
            self.sb.check_high_score()
            self.alien_explode_sound.play() # Play alien explode sfx

        # If all the aliens are shot down, delete the sprites in the group of bullets & create a new fleet of aliens
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

            # Play level up sfx
            self.level_up_sound.play()

    def _update_aliens(self):
        """
        Checks if the fleet is at the edge
            then Updates the position of all the aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Check for alien & ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to 1 alien's width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (4 * alien_width) # + 25 # adding 25 here because there was an abnormal spot left for 1 alien on screen hence reducing the margin space by trial & error. # if we wanted to do this, uncomment the +25. however since like in a classic space invader game, the alien ships move to right, drop down, move to left and drop down, we let the offset to left edge remain. it would be boring if the aliens just dropped down.
        no_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (2 * alien_height) - (1 * ship_height) # multiplying ship height by 3 because I only want to see 4 rows of aliens. as per default code its only once.
        number_rows = available_space_y // (3 * alien_height)

        # Create the rows of aliens
        for row_number in range(number_rows):
            for alien_number in range(no_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width * alien_number)
        alien.rect.x = alien.x
        alien.rect.y = alien_height + (2 * alien_height * row_number)
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any alien reaches the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet & change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by the alien"""
        if self.stats.ships_left > 1:
            # Decrease the ships left & update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens & bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet & center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _update_screen(self):
        """ Updates images on screen & flips to new image"""
        # Redraw the screen on each pass through the loop
        self.screen.fill(self.settings.bg_color) 
        # self.draw_bg() #setting a background image instead of a color
        self.ship.blitme()         
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)
        
        # draw the scoreboard
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
            
        # Make the most recently drawn screen visible
        pygame.display.flip()

 
if __name__ == "__main__":
    # Make a game instance & run the game
    ai = AlienInvasion()
    ai.run_game()