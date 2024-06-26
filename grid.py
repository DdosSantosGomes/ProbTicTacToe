import louis

class ProbTicTacToe:
    """
    Objects of this class are instances of a game of ProbTicTacToe,
    consisting of a grid of probabilities for good, neutral and bad events for each cell
    and default grid size 3.
    """
    
    def __init__(self, grid_size = 3): 
        self.grid_size = grid_size
        self.grid = self._generate_grid()

    def _generate_grid(self):
        return louis.generate_grid()
    