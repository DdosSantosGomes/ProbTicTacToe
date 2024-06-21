from grid import ProbTicTacToe
from strategies.strategy import Strategy

class Game:

    def __init__(self, grid_size = 3):
        self.instance = ProbTicTacToe(grid_size)

    def play_game(self, start, strategy : Strategy):
        pass

    def __make_move(self, player, opponent, state, cell):
        pass

    def simulate(self, player):
        pass