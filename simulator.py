import louiswork
import random
# "we" always play "x"
# "computer" always plays "o"

def playGame(move, grid, state):
    winner = louiswork.winner(state)
    print(state)
    print(winner)
    if winner == None:
        if move == "x":
            (_, cell), (_, _) = louiswork.value(grid, state)
            newstate = makeMove("x","o",state,cell,grid)
            playGame("o",grid,newstate)
        elif move == "o":
            (_, cell), (_, _) = louiswork.value(grid, state)
            newstate = makeMove("o","x",state,cell,grid)
            playGame("x",grid,newstate)
    else:
        return winner

def makeMove(player,opponent,state,cell,grid):
    success, neutral, failure = grid[cell]
    choice = random.choice(range(1,100))/100
    if choice <= success:
       return louiswork.apply(state,cell,player)
    elif choice > success and choice <= success + failure: 
       return louiswork.apply(state,cell,opponent)
    else: 
        return state


# "we" get the first move
# gameswon = 0
# for _ in range(100):
#     if playGame("x", louiswork.grid,(None,) * 9) == "x":
#         gameswon += 1


result = playGame("x",louiswork.grid,(None,) * 9)
print(result)
# "computer" gets the first move