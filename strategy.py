import random
from abc import ABC, abstractmethod
from problog_program_builder import ProbLogProgram
import strategy_helper as sh
import problog_utils
import names


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
        win_preds_per_cell = [sh.win_condition(c) for c in chosen_cells]
        clauses = []
        for win_preds_of_c in win_preds_per_cell: 
            cl = problog_utils.clause(
                head = problog_utils.function(names.WIN, problog_utils.constant(max_turns)),
                body = problog_utils.term_disj(
                    *[ problog_utils.function(win_pred, problog_utils.constant(max_turns)) for win_pred in win_preds_of_c ]
                    )
            )
            clauses.append(cl)
        return clauses

    def run(self, state, max_turns):
        """
        Runs the Problog program with the given state using each of the cells 
        from the preferred list as evidence; chooses the cell maximizing the 
        probability of winning according to the winning conditions. 
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

        for i in range(len(cells)): 
            probs[cells[i]] = self.problog_program.query(q, evidence=w_clauses[i])[win_term]

        return max(probs, key=probs.get)
    
    
