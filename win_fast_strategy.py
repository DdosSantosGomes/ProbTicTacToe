from strategy import Strategy
import names
import problog_utils
import strategy_helper as sh


class WinFastStrategy(Strategy):

    def choose_cells(self, state):
        """
        Selects a subset of the available cells; returns Problog 
        distr. string (annotated disjunction).
        """
        return sh.cells_aggressive(state, 0, mode="WF")
    

    def win_conds(self, state, chosen_cells, max_turns):
        """
        Returns a list of Problog clauses stating winning conditions for each chosen cell.
        """
        win_preds_per_cell = [sh.win_condition(c) for c in chosen_cells]
        clauses = []
        for win_preds_of_c in win_preds_per_cell: 
            cl = problog_utils.clause(
                head = problog_utils.function(names.WIN, problog_utils.constant(max_turns)),
                body = problog_utils.term_disj(*[ problog_utils.function(win_pred, problog_utils.constant(max_turns)) for win_pred in win_preds_of_c ])
            )
            clauses.append(cl)
        return clauses
    

    def do(self, state, max_turns):
        """
        Runs the Problog program 
        """

        cells = self.choose_cells(state)
        w_clauses = self.win_conds(state, cells, max_turns) 

        win_term = problog_utils.function(names.WIN, problog_utils.constant(max_turns))
        q = problog_utils.query(win_term)

        print("cells: ", cells)
        print("w_clauses: ", w_clauses)
        print("win_term: ", win_term)
        print("q: ", q)

        self.problog_program.update_choices(cells)

        probs = {}
        l = len(cells)

        for i in range(len(cells)): 
            probs[cells[i]] = self.problog_program.query(q,w_clauses[i])[win_term]

        return max(probs, key=probs.get)

        


class ConquerBoardStrategy(Strategy):

    def choose_cells(self, state):
        """
        Selects a subset of the available cells; returns Problog 
        distr. string (annotated disjunction).
        """
        cells = sh.cells_aggressive(state, 0, mode="CB")
        return sh.string_of_choice_dist(cells, 0)
    

    def win_conds(self, state, chosen_cells, max_turns):
        """
        Returns a list of Problog clauses stating winning conditions for each chosen cell.
        """
        win_preds_per_cell = [sh.win_condition(c) for c in chosen_cells]
        clauses = []
        for win_preds_of_c in win_preds_per_cell: 
            cl = problog_utils.clause(
                head = problog_utils.function(names.WIN, problog_utils.constant(max_turns)),
                body = problog_utils.term_disj(*[ problog_utils.function(win_pred, problog_utils.constant(max_turns)) for win_pred in win_preds_of_c ])
            )
            clauses.append(cl)
        return clauses
    

    def do(self, state, max_turns):
        """
        Runs the Problog program 
        """

        cells = self.choose_cells(state)

        print("cells: ", cells)

        w_clauses = self.win_conds(state, cells, max_turns) 

        
        print("w_clauses: ", w_clauses)

        win_term = problog_utils.function(names.WIN, problog_utils.constant(max_turns))
        q = problog_utils.query(win_term)

        print("win_term: ", win_term)
        print("q: ", q)

        self.problog_program.update_choices(cells)

        probs = {}
        l = len(cells)

        for i in len(cells): 
            probs[cells[i]] = self.problog_program.query(q,w_clauses[i])[win_term]

        return max(probs, key=probs.get)
    
if __name__ == "__main__":
    strategy = WinFastStrategy(None) 
    print(strategy.do(("x", "o", "x", None, None, None, "x", None, None), 2))