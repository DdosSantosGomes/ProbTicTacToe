import random 

import louiswork

from names import E, T, O, X
from strategies_aggressive import WinFast


class Game:
    """
    Simulate an arbitrary amount of games of Probabilistic Tic-Tac-Toe (default 100)
    with a given strategy, against either Louis Abraham's optimal strategy (default) or a random agent.
    """

    def __init__(self, games = 100, opposing = 'louis'):
        self.games = games
        # opposing_strategy is a function taking (grid,state) and returning the next cell to be played
        if opposing == 'random':
            self.opposing_strategy = lambda _,state : random.choice(filter(lambda cell : cell is None, state))
        elif opposing == 'louis':
            self.opposing_strategy = lambda grid,state : louiswork.value(grid,state)[1][1]
        else:
            raise UnsupportedOpposingStrategyException('The opposing strategy {} is not supported.'.format(opposing))

    def _play_one_game(self, grid, first_player, state, strategy):
        if first_player == E:
            first_player = random.choice((X,O))
        while louiswork.winner(state) == None:
            if first_player == X:
                cell = strategy.run(state) # input the strategy we use here
                print('selected move:', cell)
                state = self._make_move(X, O, state, cell, grid)
                first_player = O
            elif first_player == O:
                # (_, _), (_, cell) = louiswork.value(grid, state)
                cell = self.opposing_strategy(grid,state)
                print('selected move:', cell)
                state = self._make_move(O, X, state, cell, grid)
                first_player = X
        else:
            return louiswork.winner(state)
    
    def _make_move(self, player, opponent, state, cell, grid):
        success, _, failure = grid[cell]
        choice = random.choice(range(1, 100)) / 100
        if choice <= success:
            return louiswork.apply(state,cell,player)
        elif choice > success and choice <= success + failure: 
            return louiswork.apply(state,cell,opponent)
        else: 
            return state

    def simulate(self, player, strategy):
        """ Simulate games of ProbTicTacToe with a given starting player,
        and with the given strategy, to be passed as class constructor. """
        gameswon_x, gameswon_o, games_tied = 0, 0, 0
        for _ in range(self.games):
            grid = louiswork.generate_grid()
            s = strategy(grid)
            initial_state = (None,) * 9
            result = self._play_one_game(grid, player, initial_state, s)
            if result == X:
                gameswon_x += 1
            elif result == O:
                gameswon_o += 1
            elif result == T:
                games_tied += 1
            else:
                raise UnexpectedGameResultException('Unexpected result {}!'.format(result))
        return gameswon_x, gameswon_o, games_tied
    

class UnsupportedOpposingStrategyException(Exception):
    pass

class UnexpectedGameResultException(Exception):
    pass
    
if __name__ == "__main__":
    Game(games=1).simulate(X,WinFast)