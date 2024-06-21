import random
from abc import ABC, abstractmethod
from problog_program_builder import ProbLogProgram
import strategy_helper as sh


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
    def do(self, state, max_turns):
        pass

    def choose_cells(self, state):
        """
        Selects a subset of the available cells; returns Problog 
        distr. string (annotated disjunction).
        """
        cells = sh.cells_aggressive(state, 0, mode="WF")
        return sh.string_of_choice_dist(cells, 0)
