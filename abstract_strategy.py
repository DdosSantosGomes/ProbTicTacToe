import random
import louiswork
from abc import ABC, abstractmethod
from problog_program_builder import ProbLogProgram
from problog_utils import *
from names import *


class Strategy(ABC):

    initial_state = (None,) * 9
    
    def __init__(self, grid):
        self.grid = self.__generate_grid() if grid is None else grid
        self.problog_program = ProbLogProgram(grid)


    # only for testing
    def __generate_grid(self):
        def generate_square():
            neutral = random.choice(range(5, 35, 5))
            success = random.choice(range(30, 100 - neutral + 5, 5))
            failure = 100 - neutral - success
            return success / 100, neutral / 100, failure / 100
        return tuple(generate_square() for _ in range(9))
    

    def choice_dist(self, av_cell_nrs, turn_nr):
        """
        Returns Problog-style string of the uniform probability distribution over 
        a given list of cell numbers, given the current turn. 
        """
        total = len(av_cell_nrs)
        probs = []
        for c in av_cell_nrs:
            probs.append(probabilistic_fact(1/total, function(PLAY, c, turn_nr)))
        return annotated_disjunction(*probs)
    

    def adjacent_cells(self, cell_nr):
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
        
    def cells_aggressive(self, state, mode='WF'): 
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
            adj_cells = [c for c in self.adjacent_cells(cell) if state[c-1] == 'x']

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


    @abstractmethod
    def choose_cells(self, state):
        pass

    def win_condition(self, state, chosen_cell, player='x'): 
        """
        Returns a set of winning predicates that are reachable from the 
        current state, for this player, and for which the chosen cell contributes 
        to the winning configuration. Default: player is 'x'. Assumes 'o' is opponent.
        """

        # Indices of player's marks in winning states
        win_states = {
            "1" : ([1,2,3], WIN1, LOSE1),
            "2" : ([4,5,6], WIN2, LOSE2),
            "3" : ([7,8,9], WIN3, LOSE3),
            "4" : ([1,4,7], WIN4, LOSE4),
            "5" : ([2,5,8], WIN5, LOSE5),
            "6" : ([3,6,9], WIN6, LOSE6),
            "7" : ([1,5,9], WIN7, LOSE7),
            "8" : ([3,5,7], WIN8, LOSE8),
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
    

    def win_conds(self, state, chosen_cells, max_turns, player='x'):
        """
        Returns a list of Problog clauses stating winning conditions for each chosen cell.
        """
        win_preds_per_cell = [self.win_condition(state, c, player) for c in chosen_cells]
        clauses = []
        for win_preds_of_c in win_preds_per_cell: 
            cl = clause(
                head = function(WIN, constant(max_turns)),
                body = term_disj(
                    *[ function(win_pred, constant(max_turns)) for win_pred in win_preds_of_c ]
                    )
            )
            clauses.append(cl)
        return clauses
    
    
    def __board(self, state):
        for s in range(len(state)):
            if s == None: 
                state[s] = constant('n')
            else: 
                state[s] = constant(s)
        return function(BOARD, state)


    def run(self, state, max_turns=3):
        pass
    
    
