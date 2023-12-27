import pygame, sys
from food import Food
from snake_module import Snake
from scoreboard import Scoreboard

class SnakeGame:
    """A class to handle main snake game logic & behaviours using pygame"""

    def __init__(self):
        """Initialize the game resources & attributes"""
        pygame.init() # initialize pygame
        self.screen = pygame.display.set_mode((400,400)) # create game window
        pygame.display.set_caption("Classic Snake") # set the window title

        # Set the clock & fps
        self.clock = pygame.time.Clock()
        self.fps = 5        

        # Create instances of objects
        self.food = Food(self)
        self.sb = Scoreboard(self)
        self.snake = Snake(self)
        

    def run_game(self):
        """Main game loop"""
        while True:
            self.clock.tick(self.fps)
            self.check_events()

            self.snake.update_snake_body() # Maybe because of the way the body moves i.e. last part take location of previous part till it reaches the head, we call update_snake_body before update_snake_head
            self.snake.update_snake_head()
            
            self.snake.snake_food_collision()
            
            self.update_screen()

    def check_events(self):
        """Checks for user input like mouse/ keyboard"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if the close 'red x button' is clicked
                pygame.quit() # Quit the game window
                sys.exit()
            elif event.type == pygame.KEYDOWN: # if keyboard button is pressed down
                if event.key == pygame.K_q: # if the key 'Q' is pressed
                    pygame.quit() # Quit the game window
                    sys.exit()
                # assigning movement of snake to arrow keys
                elif event.key == pygame.K_UP and not self.snake.moving_down:
                    self.snake.moving_up = True
                    self.snake.moving_down = False
                    self.snake.moving_left = False
                    self.snake.moving_right = False
                elif event.key == pygame.K_DOWN and not self.snake.moving_up:
                    self.snake.moving_down = True
                    self.snake.moving_up = False
                    self.snake.moving_left = False
                    self.snake.moving_right = False
                elif event.key == pygame.K_LEFT and not self.snake.moving_right:
                    self.snake.moving_left = True
                    self.snake.moving_down = False
                    self.snake.moving_up = False
                    self.snake.moving_right = False
                elif event.key == pygame.K_RIGHT and not self.snake.moving_left:
                    self.snake.moving_right = True
                    self.snake.moving_down = False
                    self.snake.moving_left = False
                    self.snake.moving_up = False


    def update_screen(self):
        """Updates the screen"""
        self.screen.fill((200,230,230))
        self.snake.draw_snake()
        self.food.draw_food()
        self.sb.draw_score()

        pygame.display.update() # updates the game window



if __name__ == '__main__':
    sg = SnakeGame()
    sg.run_game()

