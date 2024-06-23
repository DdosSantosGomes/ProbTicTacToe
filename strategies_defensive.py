from abstract_strategy import Strategy
from names import *
from problog_utils import *


class TieFast(Strategy):

    def choose_cells(self, state):
        """
        Selects a preferred subset of the available cells (WF mode).
        """
        return self.cells_aggressive(state, 1, mode="WF")
    
    def run(self, state, max_turns=3):
        """
        Runs the Problog program with the given state using each of the cells 
        from the preferred list as evidence; chooses the cell minimizing the 
        probability of losing according to the losing conditions. 
        """

        self.problog_program.update_board(self.__board)
        
        cells = self.choose_cells(state)
        play_options = self.choice_dist(cells, 1)
        self.problog_program.update_play(play_options)
        
        l_clauses = self.win_conds(state, cells, max_turns, player='o') 
        lose_term = function(LOSE, constant(max_turns))
        self.problog_program.update_lose_conditions(*l_clauses)

        q = query(lose_term)
        probs = {}

        for i in range(len(cells)): 
            ev = function(PLAY, cells[i], 1)
            probs[cells[i]] = self.problog_program.query(q, evidence=ev)[lose_term]

        return min(probs, key=probs.get)
    

class ConquerBoardDefensive(Strategy):

    def choose_cells(self, state):
        """
        Selects a preferred subset of the available cells (CB mode).
        """
        return self.cells_aggressive(state, 1, mode="CB")
    
    def run(self, state, max_turns=3):
        """
        Runs the Problog program with the given state using each of the cells 
        from the preferred list as evidence; chooses the cell minimizing the 
        probability of losing according to the losing conditions. 
        """

        self.problog_program.update_board(self.__board)
        
        cells = self.choose_cells(state)
        play_options = self.choice_dist(cells, 1)
        self.problog_program.update_play(play_options)
        
        l_clauses = self.win_conds(state, cells, max_turns, player='o') 
        lose_term = function(LOSE, constant(max_turns))
        self.problog_program.update_lose_conditions(*l_clauses)

        q = query(lose_term)
        probs = {}

        for i in range(len(cells)): 
            ev = function(PLAY, cells[i], 1)
            probs[cells[i]] = self.problog_program.query(q, evidence=ev)[lose_term]

        return min(probs, key=probs.get)
    
    