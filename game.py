from grid import ProbTicTacToe
from strategies.strategy import Strategy
import random 
import strategies.louiswork as louiswork

class Game:

    def __init__(self, grid_size = 3):
        self.instance = ProbTicTacToe(grid_size)

    def play_game(self, move, state, strategy : Strategy):
        grid = self.instance.grid
        if move == "e":
            move = random.choice(("x","o"))
        while louiswork.winner(state) == None:
            if move == "x":
                (_, cell), (_, _) = louiswork.value(grid, state) # input the strategy we use here
                state = self.__make_move("x","o",state,cell)
                move == "o"
            elif move == "o":
                (_, _), (_, cell) = louiswork.value(grid, state)
                state = self.__make_move("o","x",state,cell)
                move == "x"
        else:
            return louiswork.winner(state)
    
    def __make_move(self,player,opponent,state,cell):
        grid = self.instance.grid
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