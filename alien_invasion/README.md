==== Instructions on How to Play ====
1. Install latest Python from python.org
2. Install pygame library using pip install pygame
3. Run the file 'alien_invasion.py' using the python command in the terminal.


==== Things to add ====
 - Fix the play button - Done
 - Add ship lives at top left (small red heart symbol) - Done
 - Explosion animation on alien. Fixed the explosion animation running when multiple aliens are shot (tested this by increasing the bullet width) - Done
 - Explosion animation on ship when alien & ship collide or the alien reaches the bottom - Done (One annoying thing is that the ship explosion happens after the ship_hit fn is called meaning as soon as the ship is hit, everything resets & then we see the animation)
 - Added a parameter (size) in Explosion Class to make the explosion bigger or smaller - Done
 - Add a scrolling background which moves when the game is active - Done
 - Make the aliens shoot bullets - Done
 - Add a health bar below the ship (each life can take 4 hits from aliens before losing 1 life) - Done
 - Fix ship explosion moving along with the ship when alien bullet hits it - Done
 - Added some background music & sfx like ship laser, alien explosion, damage taken by ship, level up, Ready_go sound when player clicks play button - Done
 
==== Pending ====
 - Add music & sfx - add a sound for alien_bullet shot, Game over sfx when all lives are lost
 - Set a limit to the number of bullets that can be shot by player to make the game interesting or make the ship shoot continuous bullets if the user holds down the spacebar key
 - Add a pause button by pressing escape key
 - make the aliens drop health hearts randomly upon dying (after coliding with ship, user gains health)
 - Add multiple aliens sprites (use the random module to load a random file of same size)
 - Add multiple ships
 - Save highscore in a json; make a highscore list which will have initials of the player who scored
 - Create a in-game menu (resume/pause; options; exit to desktop) - options to turnoff/ change volume, difficulty settings
 - Using the button.py file, add 2 text which inform the user to press 'p' or 'q' to start or exit the game at the bottom end of the screen when the game_state is not active