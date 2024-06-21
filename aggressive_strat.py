import strategies.louiswork as louiswork
import strategies.strategy_helper as sh

# Example (init game): uniform dist of all tiles 
# 1/9::pos(1,1); 1/9::pos(2,1); 1/9::pos(3,1); 1/9::pos(4,1); 1/9::pos(5,1); 
#                1/9::pos(6,1); 1/9::pos(7,1); 1/9::pos(8,1); 1/9::pos(9,1).

def string_for_aggressive(state, turn_nr, mode="WF"): 
    """
    Two aggressive strategies: try winning as fast as possible (by favouring tiles
    surrounded by other x's), or try 'conquering the board' (by spreading out your
    choices over the board). 

    For Winning Fast mode choose mode="WF" (default); 
    for Conquer-the-Board mode choose mode="CB". 
    """

    # If grid is empty, select all possible moves
    if state == (None,) * 9: 
        return sh.string_for_all_moves([*range(1,10)], turn_nr)

    # Get cell numbers
    cells = [c + 1 for c in louiswork.available_cells(state)]
    print("cells: ", cells)
    chosen_cells = []

    
    for cell in cells:

        # Collect adjacent cells containing an "x"
        adj_cells = [c for c in sh.adjacent_cells(cell) if state[c-1] == "x"]
        print("next to {}:".format(str(cell)), adj_cells)

        # Winning Fast: maximize number of adjacent cells containing an "x"
        if mode == "WF": 
            if len(adj_cells) > 1: 
                chosen_cells.append(cell)

        # Conquer-the-Board: minimize number of adjacent cells containing an "x" 
        elif mode == "CB":
            if len(adj_cells) <= 1:
                chosen_cells.append(cell)
            
        # Wrong mode
        else: 
            return None
        
    print("chosen: ", chosen_cells)

    # If none of the cells meet the conditions, default to all possible moves
    if chosen_cells == []: 
        return sh.string_for_all_moves([*range(1,10)], turn_nr)

    return sh.string_of_choice_dist(chosen_cells, turn_nr)


# Input max turn number in which you want to win
# Find most probable pos choice. 
def string_for_MPE(max_turn):
    return "evidence(win({}))".format(max_turn)

# Some tests
nice_state = ("x", "o", "x", None, None, None, "x", None, None)
nice_cell_nrs = [4,5,6,8,9]

# print("probdist: ", sh.string_of_prob_dist(nice_cell_nrs,2))
# print("probdist of all (should be same): ", sh.string_for_all_moves(nice_state,2))
# print("next to 6: ", sh.adjacent_cells(6))
# print("next to 5: ", sh.adjacent_cells(5))
# print("illegal: ", sh.adjacent_cells(11))
# print("winning fast: ", string_for_aggressive(nice_state, 3))
# print("conquer-the-board: ", string_for_aggressive(nice_state, 3, mode="CB"))
# print("evidence str: ",string_for_MPE(3))

    
