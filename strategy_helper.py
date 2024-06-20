import louiswork
import simulator
import game_logic

# Example (init game): uniform dist of all tiles 
# 1/9::pos(1,1); 1/9::pos(2,1); 1/9::pos(3,1); 1/9::pos(4,1); 1/9::pos(5,1); 
#                1/9::pos(6,1); 1/9::pos(7,1); 1/9::pos(8,1); 1/9::pos(9,1).


def string_of_prob_dist(av_cell_nrs, turn_nr):
    """
    Returns Problog-style string of the uniform probability distribution over 
    a given list of cell numbers, given the current turn. 
    """
    total = len(av_cell_nrs)
    probs = ""
    for i in range(total):
        probs += "1/{}::pos({},{})".format(total,av_cell_nrs[i],turn_nr)
        if i < total - 1: 
            probs += "; "
    return probs + ".\n"

# Uniform distribution containing all available moves
def string_for_all_moves(state, turn_nr):
    """
    Returns Problog-style string of the uniform probability distribution 
    over all available cells given the current state and turn. 
    """
    cells = [c + 1 for c in louiswork.available_cells(state)]
    return string_of_prob_dist(cells, turn_nr)

# Get adjacent cells on grid (hardcoded for 3x3)
def adjacent_cells(cell_nr):
    """
    Returns the cell numbers surrounding a given cell number 
    (including diagonals), on a 3x3 grid . 
    """
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

