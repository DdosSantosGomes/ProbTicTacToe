from abstract_strategy import Strategy
from names import *
from problog_utils import *


class DefensiveStrategy(Strategy):
    # note that this class is still abstract
    # as it does not define _choose_candidate_cells_to_test

    def _end_conditions(self, state, cells, player):
        return self._losing_conditions(state, cells, player)

    def _condition_term(self):
        return function(LOSE, constant(self.max_turns))

    def _choose_cell(self, probs):
        return min(probs, key=probs.get)


class TieFast(DefensiveStrategy):

    def _choose_candidate_cells_to_test(self, state):
        return self._cells_aggressive(state, mode="WF")
    

class ConquerBoardDefensive(DefensiveStrategy):

    def _choose_candidate_cells_to_test(self, state):
        return self._cells_aggressive(state, mode="CB")
    