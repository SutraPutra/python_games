import pygame, sys, time, random
from pygame import mixer
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from stats import Stats
from button import Button
from scoreboard import ScoreBoard
from explosion import Explosion
from alien_bullet import AlienBullet


class AlienInvasion():
    """A class of Alien invasion game"""

    def __init__(self):
        """Initialise all the game assets & resources"""
        pygame.init()
        self.settings = Settings(self) # create setting object
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self, 100) # create ship object & added the healthbar parameter
        self.stats = Stats(self) # create a Stats object
        self.sb = ScoreBoard(self) # create a Scoreboard object
        
        # Create Sprite Groups
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group() 
        self.alien_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        # Set clock & fps
        self.clock = pygame.time.Clock()
        self.fps = 500

        # Creating a alien by callling the function
        self.create_fleet()

        # Creating a alien shooting variable
        self.last_alien_shot = pygame.time.get_ticks()
        self.alien_cooldown = 1000 # alien_bullet cooldown in milliseconds

        # Create a play button
        self.play_button = Button(self, "Play")

        # Load the mixer & sound files
        #pygame.mixer.pre_init(44100, -16, 2, 512)
        mixer.init() # initialize the mixer library of pygame
        self.laser_sfx = pygame.mixer.Sound('sounds/laser.wav')
        self.laser_sfx.set_volume(0.25)
        self.alien_explosion_sfx = pygame.mixer.Sound('sounds/explosion.wav')
        self.alien_explosion_sfx.set_volume(0.25)
        self.ship_hit_sfx = pygame.mixer.Sound('sounds/explosion2.wav')
        self.ship_hit_sfx.set_volume(0.60)
        self.level_up_sfx = pygame.mixer.Sound('sounds/level_up_sound.wav')
        self.level_up_sfx.set_volume(0.65)
        self.ready_go_sfx = pygame.mixer.Sound('sounds/ready_go_sound.mp3')
        self.ready_go_sfx.set_volume(0.9)

        # Setting up background music, setting volume & looping for infinity
        pygame.mixer.music.load('sounds/arcade_theme_track.ogg')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)

    def run_game(self):
        """Main game loop"""
        while True:
            self.clock.tick(self.fps) # Setting a max framerate
            self._check_events()
            
            if self.stats.game_active:
                self.update_bg()
                self.ship.update() # calling update functions of all the assets in ship group
                self.update_bullet()
                self.update_alien()
                self.random_alien_shoots()
                self.update_alien_bullet()
                self.explosions.update()
            
            self._update_screen() # Drawing resources on screen


    def _check_events(self):
        """Checks for mouse & keyboard presses"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)   

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos) 

    def _check_keydown_events(self, event):
        """Helper class for refactoring code of _check_events"""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()    

    def _check_keyup_events(self, event):
        """Helper class for refactoring code of _check_events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        """Checks if the play button is clicked"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        """Starts the game if player clicks the play button or presses P button on keyboard"""
        # Reset the game settings & statistics
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_level()
        self.sb._prep_score()
        self.sb.prep_ships()
        self.stats.game_active = True

        # Empty the alien & bullet list
        self.aliens.empty()
        self.bullets.empty()

        # Create a new alien & center the player ship
        self.create_fleet()
        self.ship.center_me()

        # Play the ready go sound when the player clicks the "play" button
        self.ready_go_sfx.play()

        # Hide the cursor
        pygame.mouse.set_visible(False)

    def draw_bg(self):
        """Draws the background image of starry sky on game window"""
        for i in range(0, self.settings.tiles):
            #self.screen.blit(self.settings.bg_img, (0, i * self.settings.bg_rect.height + self.settings.scroll))
            self.screen.blit(self.settings.bg_img, (0, self.screen_rect.height - 400 - (i * self.settings.bg_rect.height) + self.settings.scroll))

    def update_bg(self):
        """Turns the static background into a scrollling background"""
        self.settings.scroll += 0.75

        if abs(self.settings.scroll) > self.settings.bg_rect.height:
            self.settings.scroll = 0

    def fire_bullet(self):
        """Creates a instance of bullet and adds it to the Sprite group bullets"""
        # We can add a limit to no. of bullets fired by setting a variable to define the limit & checking if limit is greater than the length of the no. of bullets in the bullet sprite group
        if len(self.bullets) <= 2:
            bullet = Bullet(self)
            self.bullets.add(bullet)
            self.laser_sfx.play()

    def update_bullet(self):
        """Updates the position of the bullet"""
        self.bullets.update() # using the sprite group to call the update fn of the bullet class

        # Delete the bullets which cross the top of game window
        for bullet in self.bullets.copy(): # We use a copy fn here since we can't directly alter the Sprites group
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Checks for collisions of bullets & aliens"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_hit_points * len(aliens)
                for alien in aliens: # using another for loop here to iterate over each alien in the collision values & draw explosion at its center
                    explosion = Explosion(self, alien.rect.center, size=2)
                    self.explosions.add(explosion)
                    self.alien_explosion_sfx.play()
            self.sb._prep_score()
            self.sb.check_high_score()


        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.ship.center_me()
            self.ship.hp_remaining = 100
            
            self.settings.increase_speed()
            #time.sleep(0.4) # pausing the game for dramatic effect # removed the pause since explosion animation was looking weird after shooting down the last alien on screen & game was reset
            
            self.stats.level += 1
            self.sb.prep_level()
            
            # Add the sound for Round Clear sfx
            self.level_up_sfx.play()


    def create_fleet(self): 
        # Fiding horizontal space & creating 1 single row of aliens
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.screen.get_rect().width - (2 * alien_width) # We find the horizontal space by subtracting width of 2 aliens assuming we want a margin of 1 alien width on each side of the screen.
        no_aliens_x = available_space_x // int(1.75 * alien_width) # We find the no of aliens that can actually fit inside a row while having a space of 1 alien width between each alien. Hence we divide the available space with width of 2 aliens.

        # Doing the same as above to find the vertical space & create rows of aliens
        available_space_y = self.screen.get_rect().height - alien_height - self.ship.rect.height
        no_rows = available_space_y // (4 * alien_height)

        for row_no in range(no_rows):
            for alien_no in range(no_aliens_x):
                self._create_alien(alien_no, row_no)

    def _create_alien(self, alien_no, row_no): 
        """Creates a alien at top-left edge of the screen"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        alien.x = alien_width + (2 * alien_width * alien_no)
        alien.rect.x = alien.x
        
        alien.y = alien_height + 40 + (2 * alien_height * row_no) # adding 40 here to increase distance between top edge of screen and the first upper row of aliens
        alien.rect.y = alien.y

        self.aliens.add(alien)

    def update_alien(self):
        """Updates the alien position"""
        self._check_fleet_edges()
        self.aliens.update()

        # Checks for alien & ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()

        # Checking for alien reaching the bottom
        self._check_aliens_bottom()
    
    def random_alien_shoots(self):
        """Picks a random alien & fires a bullet at player ship at regular internvals"""
        time_now = pygame.time.get_ticks()
        if time_now - self.last_alien_shot > self.alien_cooldown and len(self.alien_bullets) < 5 and len(self.aliens) > 0:
            attacking_alien = random.choice(self.aliens.sprites())
            alien_bullet = AlienBullet(self, attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            self.alien_bullets.add(alien_bullet)
            self.last_alien_shot = time_now

    def update_alien_bullet(self):
        """Updates the alien bullet"""
        self.alien_bullets.update()

        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.top >= self.screen_rect.height:
                self.alien_bullets.remove(alien_bullet)

        # Check alien bullet collision with ship
        self._check_alien_bullet_and_ship_collision()
    
    def _check_alien_bullet_and_ship_collision(self):
        """Checks for collision between alien_bullet & ship"""
        if self.ship.hp_remaining > 0:
            collided_bullet = pygame.sprite.spritecollideany(self.ship, self.alien_bullets) 
            if collided_bullet:
                self.ship_hit_sfx.play()
                self.ship.hp_remaining -= 20 # ship takes 4 hits before health becomes 0
                # Recording the exact position of the ship when the alien bullet hits the ship
                ship_pos = (self.ship.rect.centerx, self.ship.rect.centery)

                explosion = Explosion(self, self.ship.rect.center, size=1)
                self.explosions.add(explosion) 

                collided_bullet.kill() # deletes the sprite belonging to the bullets group upon collision
                # somehow this kill() also solved the explosion animation dragging on the screen whenever the player ship was hit by alien bullet
        
        else:
            self.ship_hit()
            self.alien_explosion_sfx.play() 

    def ship_hit(self):
        """Performs certain actions when ship is hit by aliens"""
        if self.stats.ship_left >= 1: # setting this to 2 makes player have 3 exact lives
            explosion = Explosion(self, self.ship.rect.center, size=3)
            self.explosions.add(explosion)
            self.stats.ship_left -= 1
            self.sb.prep_ships()
            self.bullets.empty() # empty the list of bullets
            self.aliens.empty() # empty the list of aliens
            self.create_fleet() # create the fleet 
            self.ship.center_me() # center the ship
            self.ship.hp_remaining = 100 # reset the value of the ship hp_remaining back to 100 # change this to a variable in the settings file
            time.sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Checks if the alien has reached the bottom"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break

    def _check_fleet_edges(self):
        """Responds appropriately if the alien ship reaches the ship edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_directions()
                break

    def _change_fleet_directions(self):
        """Changes fleet direction & makes the fleet drop a little"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Updates the screen on every pass through"""
        #self.screen.fill(self.settings.bg_color) # removed bg color since we added a background image
        self.draw_bg()
        self.ship.draw()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)

        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()

        for explosion in self.explosions.sprites():
            explosion.draw()

        self.sb.draw_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()