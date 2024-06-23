import random 

import louiswork

from names import E, T, O, X


class Game:
    """
    Simulate an arbitrary amount of games of Probabilistic Tic-Tac-Toe (default 100)
    with a given strategy, against either Louis Abraham's optimal strategy (default) or a random agent.
    """

    def __init__(self, strategy, opposing = 'louis', games = 100):
        self.strategy = strategy
        # opposing_strategy is a function taking (grid,state) and returning the next cell to be played
        if opposing == 'random':
            self.opposing_strategy = lambda _,state : random.choice(filter(lambda cell : cell is None, state))
        elif opposing == 'louis':
            self.opposing_strategy = lambda grid,state : louiswork.value(grid,state)[1][1]
        else:
            raise UnsupportedOpposingStrategyException('The opposing strategy {} is not supported.'.format(opposing))
        self.games = games

    def _play_one_game(self, first_player, state):
        grid = louiswork.generate_grid()
        if first_player == E:
            first_player = random.choice((X,O))
        while louiswork.winner(state) == None:
            if first_player == X:
                cell = self.strategy.run(state,3) # input the strategy we use here
                state = self._make_move(X,O,state,cell,grid)
                first_player = O
            elif first_player == O:
                # (_, _), (_, cell) = louiswork.value(grid, state)
                cell = self.opposing_strategy(grid,state)
                state = self._make_move(O,X,state,cell,grid)
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


    def simulate(self, player):
        gameswon_x, gameswon_o, games_tied = 0, 0, 0
        for _ in range(self.games):
            result = self._play_one_game(player, (None,) * 9)
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
    pass