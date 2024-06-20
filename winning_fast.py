import louiswork
import simulator
import game_logic
import strategy_helper

# Example (init game): uniform dist of all tiles 
# 1/9::pos(1,1); 1/9::pos(2,1); 1/9::pos(3,1); 1/9::pos(4,1); 1/9::pos(5,1); 
#                1/9::pos(6,1); 1/9::pos(7,1); 1/9::pos(8,1); 1/9::pos(9,1).


# Try winning as fast as possible by choosing adjacent tiles
def stringForWinningFast(state, turn_nr): 

    # If grid is empty, select all possible moves
    if state == (None,) * 9: 
        return strategy_helper.stringForAllMoves([*range(1,10)], turn_nr)

    cells = [c + 1 for c in louiswork.available_cells(state)]
    print("cells: ", cells)
    chosen_cells = []

    # Collect only cells adjacent to multiple cells with an "x"
    for cell in cells:
        adj_cells = [c for c in strategy_helper.adjacentCells(cell) if state[c-1] == "x"]
        print("next to {}:".format(str(cell)), adj_cells)
        if len(adj_cells) > 1: 
            chosen_cells.append(cell)
    
    print("chosen: ", chosen_cells)

    # If no such cells are available, default to all possible moves
    if chosen_cells == []: 
        return strategy_helper.stringForAllMoves([*range(1,10)], turn_nr)

    return strategy_helper.stringOfProbDist(chosen_cells, turn_nr)


# Input max turn number in which you want to win
# Find most probable pos choice. 
def stringForMPE(max_turn):
    return "evidence(win({}))".format(max_turn)

# Some tests
nice_state = ("x", "o", "x", None, None, None, "x", None, None)
nice_cell_nrs = [4,5,6,8,9]

# print("probdist: ", stringOfProbDist(nice_cell_nrs,2))
# print("probdist of all (should be same): ", stringForAllMoves(nice_state,2))
# print("next to 6: ", adjacentCells(6))
# print("next to 5: ", adjacentCells(5))
# print("illegal: ", adjacentCells(11))
# print("winning fast: ", stringForWinningFast(nice_state, 3))
# print("evidence str: ",stringForMPE(3))

    
