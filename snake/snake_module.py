import pygame

class Snake:
    """Class to handle the Snake head & body's assets & behaviours"""

    def __init__(self, snake_game):
        """Initialize the snake head & body & other assets"""
        self.screen = snake_game.screen
        self.screen_rect = self.screen.get_rect()
        self.food = snake_game.food
        self.sb = snake_game.sb # the scoreboard instance from main.py

        # Snake attributes
        self.snake_speed = 20

        # Create a snek head & position it
        self.snake_head = pygame.Rect(0,0, 20, 20)
        self.snake_head.center = (self.screen_rect.width/2 - 10, self.screen_rect.height/2 - 10)


        # snake head & body segments
        self.snake_body = [] # creating an empty list

        self.snake_body.append(self.snake_head)
        
        for i in range(1,3): # starts at 1 and ends at 3. hence total 2 body parts to start with
            # body_segment = pygame.Rect(self.snake_head.x - (i * 20) - (2 * i), self.snake_head.y, 20, 20)
            self.body_segment = pygame.Rect(self.snake_head.x - (i * 20) - (2 * i), self.snake_head.y, 20, 20)
            self.snake_body.append(self.body_segment)

        # store the exact location of the snake x & y position in variables for better & smoother movement
        self.x = float(self.snake_head.x)
        self.y = float(self.snake_head.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = True # setting this to True for time being. will use a game_state to start the snake moving right

    

    def update_snake_head(self):
        """Moves the snake head"""
        if self.moving_right:
            self.x += self.snake_speed
        elif self.moving_left:
            self.x -= self.snake_speed
        elif self.moving_up:
            self.y -= self.snake_speed
        elif self.moving_down:
            self.y += self.snake_speed

        self.snake_head.x = self.x # resetting the x & y pos
        self.snake_head.y = self.y

    def update_snake_body(self):
        """Moves the snake body"""
        if self.moving_down or self.moving_left or self.moving_right or self.moving_up:
            for i in range(len(self.snake_body) - 1, -0, -1):
                self.snake_body[i].x = self.snake_body[i - 1].x
                self.snake_body[i].y = self.snake_body[i - 1].y

    def grow_body(self):
        """Adds a body segment to snake_body"""
        new_segment = pygame.Rect(self.snake_body[-1].x, self.snake_body[-1].y, 20, 20)
        self.snake_body.append(new_segment)

    def snake_food_collision(self):
        """Checks for collision between snake & food"""
        collision = self.snake_head.colliderect(self.food.rect)
        
        if collision:
            self.food.create_food()
            self.grow_body()
            self.sb.score += 100
            self.sb.prep_score()


    def draw_snake(self):
        """Draw the snake on the screen"""
        for i in range(len(self.snake_body)):
            if i % 2 == 0:
                pygame.draw.ellipse(self.screen, (47,122,24), self.snake_body[i])
            else:
                pygame.draw.ellipse(self.screen, (0,0,0), self.snake_body[i])
        

        pygame.draw.ellipse(self.screen, (200,0,0), self.snake_body[0])


