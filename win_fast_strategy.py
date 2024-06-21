from strategy import Strategy
import names
import problog_utils
import strategy_helper as sh


class WinFastStrategy(Strategy):

    def choose_cells(self, state):
        """
        Selects a preferred subset of the available cells (WF mode).
        """
        return sh.cells_aggressive(state, 0, mode="WF")


class ConquerBoardStrategy(Strategy):

    def choose_cells(self, state):
        """
        Selects a preferred subset of the available cells (CB mode).
        """
        return sh.cells_aggressive(state, 0, mode="CB")
    
    
if __name__ == "__main__":
    strategy = WinFastStrategy(None) 
    print(strategy.run(("x", "o", "x", None, None, None, "x", None, None), 2))