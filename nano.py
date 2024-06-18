import random

from problog.program import PrologString

import game_logic

class ProbTicTacToe:
    """
    
    """

    def __init__(self, max_turns = 10):
        self.max_turns = max_turns
        self.program = ""
        self.build_program()
        self.problog_program = PrologString(self.program)

    def build_program(self):
        self.__grid_to_problog()
        self.__turns_to_problog()
        # idk if this is the ideal way to do it but it works
        self.program += game_logic.board
        self.program += game_logic.marks
        self.program += game_logic.positions
        self.program += game_logic.next_move
        self.program += game_logic.win_condition
        self.program += game_logic.lose_condition

    def run(self, strategy):
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
            self.program += str(p_good) + "::square" + str(i+1) + "G. "
            p_neutral = current_cell[1]
            self.program += str(p_neutral) + "::square" + str(i+1) + "N. "
            p_bad = current_cell[2]
            self.program += str(p_bad) + "::square" + str(i+1) + "B.\n"
        self.program += "\n"

    def __turns_to_problog(self):
        self.program += "%% possible turns\n"
        for turn_no in range(self.max_turns):
            self.program += "turn(" + str(turn_no) + ").\n"
        self.program += "\n"

    
class Strategy:
    pass


class Test:
    pass

if __name__ == "__main__": 
    game = ProbTicTacToe()
    print(game.program)
    # print(game.problog_program)