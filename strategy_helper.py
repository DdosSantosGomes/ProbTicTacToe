import louiswork
import simulator
import game_logic

# Example (init game): uniform dist of all tiles 
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
    cells = [c + 1 for c in louiswork.available_cells(state)]
    return stringOfProbDist(cells, turn_nr)

# Get adjacent cells on grid (hardcoded for 3x3)
def adjacentCells(cell_nr):
    if not (cell_nr in range(1,10)):
        return "Off the grid!"
    
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

    # 5 is middle cell: all cells are adjacent
    if cell_nr == 5:
        return [1,2,3,4,6,7,8,9]
    
    else:
        adj_coords = [(i-1,j), (i,j-1), (i+1,j), (i,j+1),
                        (i-1,j-1), (i-1,j+1), (i+1,j-1), (i+1,j+1)]
        adj_cells = [int(i) for i,c in coord_dict.items() if c in adj_coords]
        return adj_cells

