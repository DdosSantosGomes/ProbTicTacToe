import random
from abc import ABC, abstractmethod
from problog_program_builder import ProbLogProgram
import strategy_helper as sh
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
    
    @abstractmethod
    def choose_cells(self, state):
        pass

    def win_conds(self, state, chosen_cells, max_turns):
        """
        Returns a list of Problog clauses stating winning conditions for each chosen cell.
        """
        win_preds_per_cell = [sh.win_condition(state, c) for c in chosen_cells]
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
        """
        Runs the Problog program with the given state using each of the cells 
        from the preferred list as evidence; chooses the cell maximizing the 
        probability of winning according to the winning conditions. 
        """

        self.problog_program.update_board(self.__board)
        
        cells = self.choose_cells(state)
        play_options = sh.choice_dist(cells, 1)
        self.problog_program.update_play(play_options)
        
        w_clauses = self.win_conds(state, cells, max_turns) 
        win_term = function(WIN, constant(max_turns))
        self.problog_program.update_win_conditions(*w_clauses)

        q = query(win_term)
        probs = {}

        for i in range(len(cells)): 
            ev = function(PLAY, cells[i], 1)
            probs[cells[i]] = self.problog_program.query(q, evidence=ev)[win_term]

        return max(probs, key=probs.get)
    
    
