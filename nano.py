import random

from problog.program import PrologString
from problog import get_evaluatable

import game_logic

class ProbTicTacToe:
    """
    
    """

    def __init__(self, max_turns = 10):
        self.max_turns = max_turns
        self.program = ""
        self.build_program()
        self.program += "query(win(1))."
        self.problog_program = PrologString(self.program)

    def build_program(self):
        self.__grid_to_problog()
        self.__turns_to_problog()
        # idk if this is the ideal way to do it but it works
        self.program += game_logic.board
        # self.program += game_logic.marks
        self.program += game_logic.positions # needs to be fixed
        self.program += game_logic.next_move
        self.program += game_logic.win_condition
        self.program += game_logic.lose_condition

    def run(self, strategy):
        """Test a single game with a given strategy against the AI"""
        pass

    def __generate_grid(self):
        def generate_square():
            neutral = random.choice(range(5, 35, 5))
            success = random.choice(range(30, 100 - neutral + 5, 5))
            failure = 100 - neutral - success
            return success / 100, neutral / 100, failure / 100
        return tuple(generate_square() for _ in range(9))
    
    def __grid_to_problog(self):
        self.program += "%% probabilities for each square\n"
        grid = self.__generate_grid()
        for i in range(9): # iterate over the cells
            current_cell = grid[i]
            p_good = current_cell[0]
            self.program += str(p_good) + "::square" + str(i+1) + "good(N). "
            p_neutral = current_cell[1]
            self.program += str(p_neutral) + "::square" + str(i+1) + "neutral(N). "
            p_bad = current_cell[2]
            self.program += str(p_bad) + "::square" + str(i+1) + "bad(N).\n"
        self.program += "\n"

    def __turns_to_problog(self):
        self.program += "%% possible turns\n"
        for turn_no in range(1, self.max_turns + 1):
            player = "x" if turn_no % 2 == 1 else "o"
            self.program += "turn(" + player + "," + str(turn_no) + ").\n"
        self.program += "\n"

    
class Strategy:
    pass


class Test:
    pass

if __name__ == "__main__": 
    game = ProbTicTacToe()
    # get_evaluatable().create_from(game.problog_program).evaluate()
    print(game.program)