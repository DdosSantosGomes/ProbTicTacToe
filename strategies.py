import louiswork
import simulator
import game_logic

# 1/9::pos(1,1); 1/9::pos(2,1); 1/9::pos(3,1); 1/9::pos(4,1); 1/9::pos(5,1); 
#                1/9::pos(6,1); 1/9::pos(7,1); 1/9::pos(8,1); 1/9::pos(9,1).

# Returns Problog-style string of unif. prob. dist. given list of available cell nrs
def stringOfProbDist(av_cell_nrs, turn_nr):
    total = len(av_cell_nrs)
    probs = ""
    for i in range(total):
        probs += "1/{}::pos({},{})".format(total,av_cell_nrs[i],turn_nr)
        if i < total - 1: 
            probs += "; "
    return probs + ".\n"

# Uniform distribution containing all available moves
def stringForAllMoves(state, turn_nr):
    cells = louiswork.available_cells(state)
    return stringOfProbDist(map(+1, cells), turn_nr)

# Get adjacent cells on grid (hardcoded for 3x3)
def adjacentCells(cell_nr):
    if not (cell_nr in range(9)):
        print("Off the grid!")
        return []
    
    coord_dict = {
        "1" : (1,1),
        "2" : (2,1),
        "3" : (3,1),
        "4" : (1,2),
        "5" : (2,2), 
        "6" : (3,2),
        "7" : (1,3),
        "8" : (2,3),
        "9" : (3,3)
    } 
    
    (i,j) = coord_dict[str(cell_nr)]

    # 5 is middle cell
    if cell_nr == 5:
        adj_coords = range(1,9)
    else:
        adj_coords = [(i-1,j), (i,j-1), (i+1,j), (i,j+1),
                        (i-1,j-1), (i-1,j+1), (i+1,j-1), (i+1,j+1)]
    adj_cells = [int(i) for i,c in coord_dict.items() if c in adj_coords]

    return adj_cells


# Try winning as fast as possible by choosing adjacent tiles
def stringForWinningFast(state, turn_nr): 

    # If grid is empty, select all possible moves
    if state == (None,) * 9: 
        return stringForAllMoves(range(1,9), turn_nr)

    cells = louiswork.available_cells(state)
    chosen_cells = []

    # Collect cells adjacent to multiple cells with an "x"
    for cell in cells:
        adj_cells = [c for c in adjacentCells(cell) if c == "x"]
        print(adj_cells)
        if len(adj_cells) > 1: 
            chosen_cells += cell 
    
    print("chosen: ", chosen_cells)

    # If no such cells are available, select all possible moves
    if chosen_cells == []: 
        return stringForAllMoves(range(1,9), turn_nr)

    return stringOfProbDist(chosen_cells, turn_nr)


# Input max turn number in which you want to win
# Find most probable pos choice. 
def stringForMPE(max_turn):
    return "evidence(win({}))".format(max_turn)



nice_state = ("x", "o", "x", None, None, None, "x", None, None)
nice_cell_nrs = louiswork.available_cells(nice_state)

print("propbdist: ", stringOfProbDist(nice_cell_nrs,2))
print(louiswork.available_cells(nice_state))
print("probdist of all: ", stringForAllMoves(nice_state,2))
print("next to 5: ", adjacentCells(5))
print("illegal: ", adjacentCells(11))
print("winning fast: ", stringForWinningFast(nice_state, 3))
print("evidence str: ",stringForMPE(3))

    
