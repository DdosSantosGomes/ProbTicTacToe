from abc import ABC, abstractmethod

import louiswork
from problog_program_builder import ProbLogProgram
from problog_utils import *
from names import *


class Strategy(ABC):
    """
    Base abstract Strategy class - in a nutshell, a wrapper for the run function,
    which calculates the optimal move according to a strategy, from a given state,
    with a default lookahead of 3 turns.
    """
    
    def __init__(self, grid, max_turns = 3):
        self.grid = grid
        self.max_turns = max_turns
        self.problog_program = ProbLogProgram(grid, max_turns)

    def run(self, state):
        """ Calculates the optimal move according to a strategy from a given state. """
        ### pipeline: update ProbLog program -> query it -> find optimal cell
        # first: update the state of the board in ProbLog
        self.problog_program.update_board(self._board(state)) 
        # second: tell ProbLog which cells are available to play in
        candidate_cells = self._choose_candidate_cells_to_test(state)
        play_options = self._choice_dist(candidate_cells)
        self.problog_program.update_play(play_options)
        # third: specify end conditions to ProbLog
        end_condition_clauses = self._end_conditions(state, candidate_cells, player=X) 
        end_condition_term = self._condition_term()
        # self.problog_program.update_end_conditions(*end_condition_clauses)
        # end_condition_query = query(end_condition_term)
        end_condition_query = 'query(win(3)).'
        probs = {} # dict of key = cell and value = probability of reaching the desired end condition
        ### next: query the ProbLog program with evidence of playing the candidate cells
        for cell in candidate_cells: 
            ev = evidence(function(PLAY, constant(cell), constant(1)))

            # print('state:', state)
            # print('cells to choose from:', candidate_cells)
            # print('key:', end_condition_term + str(type(end_condition_term)))

            prob = self.problog_program.query(end_condition_query, evidence=ev)

            # print('result:', prob)

            probs[cell] = prob
        ### last: find the optimal cell to play, and send it back to the Game simulator
        return self._choose_cell(probs)
    
    @abstractmethod
    def _choose_candidate_cells_to_test(self, state):
        """ Select a subset of candidate cells to test. """
        pass

    @abstractmethod
    def _end_conditions(self, state, cells, player):
        pass

    @abstractmethod
    def _condition_term(self):
        pass

    @abstractmethod
    def _choose_cell(self, probs):
        """ Choose a cell to play, according to our strategy. """
        pass

    def _choice_dist(self, av_cell_nrs):
        """ Returns a ProbLog annotated disjunction with body, consisting of the
        uniform probability distribution over a given list of cell numbers.
        This encodes the possible choices we are allowed to make in ProbLog. """
        total = len(av_cell_nrs)
        probs = []
        for c in av_cell_nrs:
            probs.append(
                probabilistic_fact(
                    prob = 1/total, 
                    f = function(PLAY, constant(c), variable(A))))
        return annotated_disjunction_with_body(
            annotated_disj = annotated_disjunction(*probs),
            body = function(TURN, ANY, variable(A))
        )

    
    def _adjacent_cells(self, cell_nr, state):
        """ Returns the cell numbers surrounding a given cell number (including diagonals), on a 3x3 grid. """
        if not (cell_nr in range(1,10)):
            raise IndexOutOfBoundsException('Off the grid! {} should be an int between 1-9'.format(cell_nr))
        coord_dict = {
            "1" : (1,1), "2" : (2,1), "3" : (3,1),
            "4" : (1,2), "5" : (2,2), "6" : (3,2),
            "7" : (1,3), "8" : (2,3), "9" : (3,3)
        } 
        (i,j) = coord_dict[str(cell_nr)]
        if cell_nr == 5: # 5 is middle cell: all cells are adjacent
            return [ c + 1 for c in louiswork.available_cells(state) ]
        else:
            adj_coords = [(i-1,j), (i,j-1), (i+1,j), (i,j+1),
                            (i-1,j-1), (i-1,j+1), (i+1,j-1), (i+1,j+1)]
            adj_cells = [ int(i) for i,c in coord_dict.items() if c in adj_coords ]
            return adj_cells
        
    def _cells_aggressive(self, state, mode='WF'): 
        """ Two aggressive strategies: try winning as fast as possible (by favouring tiles
        surrounded by other x's), or try 'conquering the board' (by spreading out your
        choices over the board). Returns a list of chosen cells.

        For Winning Fast mode choose mode="WF" (default); 
        for Conquer-the-Board mode choose mode="CB". """
        if state == (None,) * 9: # If grid is empty, select all possible moves
            return list(range(1,10))
        cells = [ c + 1 for c in louiswork.available_cells(state) ]
        chosen_cells = []
        for cell in cells:
            adj_cells = [ c for c in self._adjacent_cells(cell, state) if state[c-1] == X ]
            if mode == 'WF': # maximize number of adjacent cells containing an x
                if len(adj_cells) > 1: 
                    chosen_cells.append(cell)
            elif mode == 'CB': # minimize number of adjacent cells containing an "x" 
                if len(adj_cells) <= 1:
                    chosen_cells.append(cell)
            else: 
                return None
        if chosen_cells == []: # If none of the cells meet the conditions, default to all available cells
            return [ c + 1 for c in louiswork.available_cells(state) ]
        return chosen_cells 
    
    def _win_conditons_for_chosen_cells(self, state, chosen_cells, player='x'):
        """ Returns a list of ProbLog clauses, stating winning conditions for each chosen cell. """
        win_preds_per_cell = [ self._win_condition_for_cell(state, c, player) for c in chosen_cells ]   
        clauses = []
        for win_preds_of_c in win_preds_per_cell: 
            if win_preds_of_c == []: 
                b = "" # Return an empty body for cells that can't contribute to a win
            else:
                b = term_disj(
                        *[ function(win_pred, constant(self.max_turns)) for win_pred in win_preds_of_c ]
                        )
                
            cl = clause(
                head = function(WIN, constant(self.max_turns)),
                body = b
            )
            clauses.append(cl)
        return clauses
    
    def _win_condition_for_cell(self, state, chosen_cell, player='x'): 
        """ Returns a set of winning predicates that are reachable from the 
        current state, for this player, and for which the chosen cell contributes 
        to the winning configuration. Default: player is 'x'. Assumes 'o' is opponent. """
        win_states = { # Indices of player's marks in winning states
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
                if player == X: # Don't count winning condition if it is unreachable
                    for i in winning_indices: 
                        if state[i-1] == O:
                            impossible = True
                            break
                else: 
                    for i in winning_indices: 
                        if state[i-1] == X:
                            impossible = True
                            break
                if not impossible: 
                    if player == X:
                        possible_wins.append(win_states[w][1]) 
                    else:
                        possible_wins.append(win_states[w][2]) 
        return possible_wins

    def _board(self, state):
        """ Returns a ProbLog fact encoding the current state of the board. """
        new_state = []
        for cell_nr in range(1, 10):
            current_state = state[cell_nr - 1]
            if current_state == None: 
                new_state.append(
                    fact(function(BOARD, constant(cell_nr), constant(N), 0))
                )
            else: 
                new_state.append(
                    fact(function(BOARD, constant(cell_nr), constant(current_state), 0))
                )
        return new_state
    

class IndexOutOfBoundsException(Exception):
    pass

class UnsupportedStrategyException(Exception):
    pass