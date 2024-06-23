from abstract_strategy import Strategy
from strategies_defensive import *
from names import *
from problog_utils import *


class WinFast(Strategy):

    def choose_cells(self, state):
        """
        Selects a preferred subset of the available cells (WF mode).
        """
        return self.cells_aggressive(state, 1, mode="WF")
    
    def run(self, state, max_turns=3):
        """
        Runs the Problog program with the given state using each of the cells 
        from the preferred list as evidence; chooses the cell maximizing the 
        probability of winning according to the winning conditions. 
        """

        self.problog_program.update_board(self.__board)
        
        cells = self.choose_cells(state)
        play_options = self.choice_dist(cells, 1)
        self.problog_program.update_play(play_options)
        
        w_clauses = self.win_conds(state, cells, max_turns, player='x') 
        win_term = function(WIN, constant(max_turns))
        self.problog_program.update_win_conditions(*w_clauses)

        q = query(win_term)
        probs = {}

        for i in range(len(cells)): 
            ev = function(PLAY, cells[i], 1)
            probs[cells[i]] = self.problog_program.query(q, evidence=ev)[win_term]

        return max(probs, key=probs.get)


class ConquerBoardAggressive(Strategy):

    def choose_cells(self, state):
        """
        Selects a preferred subset of the available cells (CB mode).
        """
        return self.cells_aggressive(state, 1, mode="CB")
    
    def run(self, state, max_turns=3):
        """
        Runs the Problog program with the given state using each of the cells 
        from the preferred list as evidence; chooses the cell maximizing the 
        probability of winning according to the winning conditions. 
        """

        self.problog_program.update_board(self.__board)
        
        cells = self.choose_cells(state)
        play_options = self.choice_dist(cells, 1)
        self.problog_program.update_play(play_options)
        
        w_clauses = self.win_conds(state, cells, max_turns, player='x') 
        win_term = function(WIN, constant(max_turns))
        self.problog_program.update_win_conditions(*w_clauses)

        q = query(win_term)
        probs = {}

        for i in range(len(cells)): 
            ev = function(PLAY, cells[i], 1)
            probs[cells[i]] = self.problog_program.query(q, evidence=ev)[win_term]

        return max(probs, key=probs.get)
    
if __name__ == "__main__":
    strategy = WinFast(None) 
    print(strategy.run(("x", "o", "x", None, None, None, "x", None, None), 2))