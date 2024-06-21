import random

class ProbTicTacToe:
    """
    Objects of this class are instances of a game of ProbTicTacToe
    with attributes grid_size, max_turns and grid.
    """
    
    def __init__(self, grid_size = 3): 
        self.grid_size = grid_size
        self.grid = self.__generate_grid()

    def __generate_grid(self):
        def generate_square():
            neutral = random.choice(range(5, 35, 5))
            success = random.choice(range(30, 100 - neutral + 5, 5))
            failure = 100 - neutral - success
            return success / 100, neutral / 100, failure / 100
        return tuple(generate_square() for _ in range(self.grid_size ** 2))
    