import random

from abc import ABC, abstractmethod

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


class Game:

    def __init__(self, grid_size = 3):
        self.instance = ProbTicTacToe(grid_size)

    def play_game(self, start, strategy):
        pass

    def __make_move(self, player, opponent, state, cell):
        pass

    def simulate(self, player):
        pass


# term names, centralized
SQUARE_GOOD = 'square_good'
SQUARE_NEUTRAL = 'square_neutral'
SQUARE_BAD = 'square_bad'
TURN = 'turn'
BOARD = 'board'
CHOOSE = 'choose'
WIN = 'win'
LOSE = 'lose'

class ProbLogProgram:

    __program = {}
    """
    This is a dictionary indexed by the sections of our ProbLog program.
    In particular, our indices are:
        - board
        - grid
        - turns
        - moves
        - win
        - lose \n
    and they correspond to the fixed game logic of the game of ProbTicTacToe. \n
    This is an internal representation which should be kept hidden.
    """
    
    def __init__(self):
        pass

    def query(self, *queries):
        pass

    def __str__(self): # the pretty function from stackoverflow
        pass


class Strategy(ABC):
    
    @abstractmethod
    def do(self, state):
        pass

class AggressiveStrategy(Strategy):

    def do(self, state):
        pass

