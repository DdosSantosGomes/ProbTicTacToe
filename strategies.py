import louiswork
import simulator
import game_logic

# 1/9::pos(1,1); 1/9::pos(2,1); 1/9::pos(3,1); 1/9::pos(4,1); 1/9::pos(5,1); 
#                1/9::pos(6,1); 1/9::pos(7,1); 1/9::pos(8,1); 1/9::pos(9,1).

# Uniform distribution containing all available moves
def stringForUniDist(state, turn_nr):
    cells = louiswork.available_cells(state)
    total = len(cells)
    probs = ""
    for i in range(total):
        probs += "1/{}::pos({},{})".format(total,str(i),turn_nr)
        if i < total - 1: 
            probs += "; "
    return probs + ".\n"

# Get adjacent cells on grid (hardcoded for 3x3)
def adjacentCells(cell):
    if not (cell in range(9)):
        return []
    
    coord_dict = {
        "1" : (1,1),
        "2" : (1,2),
        "3" : (1,3),
        "4" : (2,1),
        "5" : (2,2), 
        "6" : (2,3),
        "7" : (3,1),
        "8" : (3,2),
        "9" : (3,3)
    } 
    
    (i,j) = coord_dict[cell]
    adj_coords = [(i-1,j), (i,j-1), (i+1,j), (i,j+1)]
    adj_cells = [i for i,c in coord_dict.iteritems() if c in adj_coords]

    return adj_cells


# Try winning as fast as possible by choosing adjacent tiles
def stringForWinningFast(state, turn_nr): 
    cells = louiswork.available_cells(state)
    for cell in cells:
        adj_cells = adjacentCells(cell)
        if any()


# Input max turn number in which you want to win
# Find most probable pos choice. 
def stringForMPE(max_turn):
    return "evidence(win({}))".format(max_turn)





print(stringForUniDist((None,"x",None,"o"),2))

    
