from grid import ProbTicTacToe
from abstract_strategy import Strategy
from strategies import WinFastStrategy
import random 
import louiswork as louiswork

class Game:

    def __init__(self):
        pass

    def play_game(self, move, state, strategy):
        grid = louiswork.generate_grid()
        s = strategy(grid)
        # if strategy == 'WF':
        #     s = WinFastStrategy(grid)
        # else:
        #     raise Exception()
        if move == "e":
            move = random.choice(("x","o"))
        while louiswork.winner(state) == None:
            if move == "x":
                cell = s.run(state,3) # input the strategy we use here
                state = self.__make_move("x","o",state,cell,grid)
                move = "o"
            elif move == "o":
                (_, _), (_, cell) = louiswork.value(grid, state)
                state = self.__make_move("o","x",state,cell,grid)
                move = "x"
        else:
            return louiswork.winner(state)
    
    def __make_move(self,player,opponent,state,cell,grid):
        success, neutral, failure = grid[cell]
        choice = random.choice(range(1,100))/100
        if choice <= success:
            return louiswork.apply(state,cell,player)
        elif choice > success and choice <= success + failure: 
            return louiswork.apply(state,cell,opponent)
        else: 
            return state


    def simulate(self,player,strategy):
        gameswonx = 0
        gameswono = 0
        gamestied = 0 
        for _ in range(1000):
            result = self.play_game(player,(None,) * 9,strategy)
            if result == "x":
                gameswonx += 1
            elif result == "o":
                gameswono += 1
            elif result == "t":
                gamestied += 1
            else:
                print("error")
        return gameswonx, gameswono, gamestied
    
if __name__ == "__main__":
    game = Game()
    game.simulate('x',WinFastStrategy)