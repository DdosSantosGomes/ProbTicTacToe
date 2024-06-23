import louiswork 
import names
from problog_utils import *
from names import *

def choice_dist(av_cell_nrs, turn_nr):
    """
    Returns Problog-style string of the uniform probability distribution over 
    a given list of cell numbers, given the current turn. 
    """
    total = len(av_cell_nrs)
    probs = []
    for c in av_cell_nrs:
        probs.append(probabilistic_fact(1/total, function(PLAY, c, turn_nr)))
    return annotated_disjunction(*probs)


def choice_dist_all_moves(state, turn_nr):
    """
    Returns Problog-style string of the uniform probability distribution 
    over all available cells given the current state and turn. 
    """
    cells = [c + 1 for c in louiswork.available_cells(state)]
    return choice_dist(cells, turn_nr)


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
    

def cells_aggressive(state, turn_nr, mode='WF'): 
    """
    Two aggressive strategies: try winning as fast as possible (by favouring tiles
    surrounded by other x's), or try 'conquering the board' (by spreading out your
    choices over the board). Returns a set of chosen cell numbers.

    For Winning Fast mode choose mode="WF" (default); 
    for Conquer-the-Board mode choose mode="CB". 
    """

    # If grid is empty, select all possible moves
    if state == (None,) * 9: 
        return [*range(1,10)]

    # Get cell numbers
    cells = [c + 1 for c in louiswork.available_cells(state)]
    chosen_cells = []

    for cell in cells:

        # Collect adjacent cells containing an "x"
        adj_cells = [c for c in adjacent_cells(cell) if state[c-1] == 'x']

        # Winning Fast: maximize number of adjacent cells containing an "x"
        if mode == 'WF': 
            if len(adj_cells) > 1: 
                chosen_cells.append(cell)

        # Conquer-the-Board: minimize number of adjacent cells containing an "x" 
        elif mode == 'CB':
            if len(adj_cells) <= 1:
                chosen_cells.append(cell)
            
        # Wrong mode
        else: 
            return None

    # If none of the cells meet the conditions, default to all possible moves
    if chosen_cells == []: 
        return [*range(1,10)]

    return chosen_cells 


def win_condition(state, chosen_cell, player='x'): 
    """
    Returns a set of winning predicates that are reachable from the 
    current state, for this player, and for which the chosen cell contributes 
    to the winning configuration. Default: player is 'x'. Assumes 'o' is opponent.
    """

    # Indices of player's marks in winning states
    win_states = {
        "1" : ([1,2,3], names.WIN1, names.LOSE1),
        "2" : ([4,5,6], names.WIN2, names.LOSE2),
        "3" : ([7,8,9], names.WIN3, names.LOSE3),
        "4" : ([1,4,7], names.WIN4, names.LOSE4),
        "5" : ([2,5,8], names.WIN5, names.LOSE5),
        "6" : ([3,6,9], names.WIN6, names.LOSE6),
        "7" : ([1,5,9], names.WIN7, names.LOSE7),
        "8" : ([3,5,7], names.WIN8, names.LOSE8),
    }

    possible_wins = []
    impossible = False

    for w in win_states:
        winning_indices = win_states[w][0]
        if chosen_cell in winning_indices: 
            impossible = False

            # Don't count winning condition if it is unreachable
            if player == 'x':
                for i in winning_indices: 
                    if state[i-1] == 'o':
                        impossible = True
                        break

            else: 
                for i in winning_indices: 
                    if state[i-1] == 'x':
                        impossible = True
                        break
                
            if impossible == False: 
                if player == 'x':
                    possible_wins.append(win_states[w][1]) 
                else:
                    possible_wins.append(win_states[w][2]) 

    return possible_wins


# Some tests
nice_state = ('x', 'o', 'x', None, None, None, 'x', None, None)
nice_cell_nrs = [4,5,6,8,9]

# print("probdist: ", string_of_choice_dist(nice_cell_nrs,2))
# print("probdist of all (should be same): ", string_for_all_moves(nice_state,2))
# print("next to 6: ", adjacent_cells(6))
# print("next to 5: ", adjacent_cells(5))
# print("illegal: ", adjacent_cells(11))
# print("winning fast: ", cells_aggressive(nice_state, 3))
# print("conquer-the-board: ", cells_aggressive(nice_state, 3, mode="CB"))
print(choice_dist(nice_cell_nrs,1))



