from strategy import Strategy
from ..problog_program import names
from ..problog_program import utils
import strategy_helper as sh


class WinFastStrategy(Strategy):

    def choose_cells(self, state):
        """
        Selects a subset of the available cells; returns Problog 
        distr. string (annotated disjunction).
        """
        cells = sh.cells_aggressive(state, 0, mode="WF")
        return sh.string_of_choice_dist(cells, 0)
    
    # def list_board_repr(self, state, chosen_cells): 
    #     # Here put the lines/strings saying what the board should look like after putting 
    #     # an x at each chosen_cells
    #     new_board = 
    #     return [utils.function(names.BOARD, )]

    def win_conds(self, state, chosen_cells, max_turns):
        """
        Returns a list of Problog clauses stating winning conditions for each chosen cell.
        """
        win_preds_per_cell = [sh.win_condition(state, c) for c in chosen_cells]
        clauses = []
        for win_preds_of_c in win_preds_per_cell: 
            cl = utils.clause(
                head = utils.function(names.WIN, utils.constant(max_turns)),
                body = utils.term_disj(*[ utils.function(win_pred, utils.constant(max_turns)) for win_pred in win_preds_of_c ])
            )
            clauses.append(cl)
        return clauses
    

    def make_decision(self, state, max_turns):
        """
        Runs the Problog program 
        """

        cells = self.choose_cells(self.state)
        w_clauses = self.win_conds(self, state, cells, max_turns) 

        win_term = utils.function(names.WIN, utils.constant(max_turns))
        q = utils.query(win_term)

        self.problog_program.update_choices(cells)

        probs = {}
        l = len(cells)

        for i in len(cells): 
            probs[cells[i]] = self.problog_program.query(q,w_clauses[i])[win_term]

        return max(probs, key=probs.get)
        


class ConquerBoardStrategy(Strategy):

    def choose_cells(self, state):
        return sh.string_for_aggressive(state, 0, mode="CB")
    
    def list_board_repr(self, chosen_cells): 
        # Here put the lines/strings saying what the board should look like after putting 
        # an x at each chosen_cells
        pass

    def win_conds(self, state, chosen_cells):
        return [sh.win_condition(state, c) for c in chosen_cells]
    
if __name__ == "__main__":
    strategy = WinFastStrategy(None) 
    strategy.choose_cells(strategy.initial_state)