Things to fix:
 - There is a bug in the movement of snake. The snakes still moves back on itself. example: if the snake is moving_up. I can but the right and down button quickly and then the snake instead of moving right & down , simply moves down.
 - No way to end the game currently
 - Make it so that the tail of the snake never changes color. new growth only happens only on -2 of the snake body (refer to the grow fn in snake_module)
 - Add a play button
 - High score. User input of 3 initials.
 - Menu system

 Fixed:
 - Since the food rect size is 20 by 20. food properly appears (randomly) on a 20 by 20 grid.
 - the snake is moving in a smooth manner. it should jump to the distance of its side.for ex. if the square is of 20 by 20. then when any movement key is pressed, it should shift to 20 px in that direction. Current temporary fix is to remove the movement flag & move the snake head manually 20 px. Need to add a timer maybe to control the speed. fixed it by reducing the fps of the game and keeping the movement flags 
 - Start the game with 2 snake segments
 - At the start of the game the same can go over itself if we start with the left arrow key
 - Added a score system. Created a Scoreboard class.
