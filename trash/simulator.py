import louiswork as louiswork
import random
# "we" always play "x"
# "computer" always plays "o"

def play_game(move, strategy):
    state = (None,) * 9
    grid = louiswork.generate_grid()
    if move == "e":
        move = random.choice(("x","o"))
    while louiswork.winner(state) == None:
        if move == "x":
            cell = strategy(grid, state) # input the strategy we use here
            state = make_move("x","o",state,cell,grid)
            move = "o"
        elif move == "o":
            (_, _), (_, cell) = louiswork.value(grid, state)
            state = make_move("o","x",state,cell,grid)
            move = "x"
    else:
        return louiswork.winner(state)
    
def make_move(player,opponent,state,cell,grid):
    success, neutral, failure = grid[cell]
    choice = random.choice(range(1,100))/100
    if choice <= success:
       return louiswork.apply(state,cell,player)
    elif choice > success and choice <= success + failure: 
       return louiswork.apply(state,cell,opponent)
    else: 
        return state

def simulate(player,strategy):
    gameswonx = 0
    gameswono = 0
    gamestied = 0 
    for _ in range(1000):
        result = play_game(player, strategy)
        if result == "x":
            gameswonx += 1
        elif result == "o":
            gameswono += 1
        elif result == "t":
            gamestied += 1
        else:
            print("error")
    return gameswonx, gameswono, gamestied

def louis_strategy(grid,state):
    (_, cell), (_, _) = louiswork.value(grid, state)
    return cell

def random_strategy(grid,state):
    return random.choice(louiswork.available_cells(state))

# def naive_strategy(grid,state):
#     probabilities = 0
#     cells = louiswork.available_cells(state)
#     for prob in grid:
#         probwin = prob[1]
#         probabilities.append(cell, probwin) 
#     return cells[probabilities.index(max(probabilities))]

    
print(simulate("x",random_strategy))
# "computer" gets the first move