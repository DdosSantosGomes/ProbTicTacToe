from abstract_strategy import Strategy
from strategies_defensive import *
from names import *
from problog_utils import *


class AggressiveStrategy(Strategy):
    # note that this class is still abstract
    # as it does not define _choose_candidate_cells_to_test
    
    def _end_conditions(self, state, cells, player):
        return self._win_conditons_for_chosen_cells(state, cells, player)

    def _condition_term(self):
        return function(WIN, constant(self.max_turns))

    def _choose_cell(self, probs):
        return max(probs, key=probs.get)


class WinFast(AggressiveStrategy):

    def _choose_candidate_cells_to_test(self, state):
        return self._cells_aggressive(state, mode="WF")


class ConquerBoardAggressive(AggressiveStrategy):

    def _choose_candidate_cells_to_test(self, state):
        return self._cells_aggressive(state, mode="CB")
    