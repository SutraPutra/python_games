class Stats():
    """Class to hold stats of game"""

    def __init__(self, ai_game):
        """Initialise the stats"""
        self.settings = ai_game.settings

        self.reset_stats()
        
        self.game_active = False # main game loop flag

        self.high_score = 0 # high score should never be reset.
        
        


    def reset_stats(self):
        """Reset the stats at the start of the game"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    # commented code is needed to add the save & load high score functionality
    #     
    # def save_high_score(self):
    #     """Saves the high score to a JSON file"""
    #     high_score_data = {"high_score" : self.high_score}

    #     with open('high_score.json', 'w') as f:
    #         json.dump(high_score_data, f)

    # def load_high_score(self):
    #     """Loads the high score from the JSON file"""
    #     try:
    #         with open('high_score.json', 'r') as f:
    #             high_score_data = json.load(f)
    #             self.high_score = high_score_data.get("high_score", 0)
    #     except FileNotFoundError:
    #         # If the file is not found, set the high score to 0
    #         self.high_score = 0