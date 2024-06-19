import random

from problog.program import PrologString
from problog import get_evaluatable


class ProbTicTacToe:
    """
    
    """

    def __init__(self, grid_size = 3, max_turns = None): 
        self.grid_size = grid_size
        self.max_turns = self.grid_size ** 2 + 1 if max_turns is None else max_turns
        self.program = ""
        self.__build_program()

    def __build_program(self):
        self.__grid()
        self.__turns()
        self.__board()
        self.__moves()
        self.__win_condition()
        self.__lose_condition()

    def run(self, strategy): # Test a single game with a given strategy against the AI
        pass

    def query(self, *queries): # query the ProbLog program. Give the queries in ProbLog syntax
        for query in queries:
            self.program += "query({q}).".format(q = query)
        try:
            result = get_evaluatable().create_from(PrologString(self.program)).evaluate()
            return result
        except:
            raise Exception("Please give the queries in valid ProbLog syntax (e.g. 'win(2)')!")

    def __generate_grid(self):
        def generate_square():
            neutral = random.choice(range(5, 35, 5))
            success = random.choice(range(30, 100 - neutral + 5, 5))
            failure = 100 - neutral - success
            return success / 100, neutral / 100, failure / 100
        return tuple(generate_square() for _ in range(self.grid_size ** 2))
    
    def __grid(self):
        self.program += "%% probabilities for each square\n"
        grid = self.__generate_grid()
        for i in range(self.grid_size ** 2): # iterate over the cells
            current_cell = grid[i]
            p_good = current_cell[0]
            self.program += str(p_good) + "::square" + str(i+1) + "good(N); "
            p_neutral = current_cell[1]
            self.program += str(p_neutral) + "::square" + str(i+1) + "neutral(N); "
            p_bad = current_cell[2]
            self.program += str(p_bad) + "::square" + str(i+1) + "bad(N).\n"
        self.program += "\n"

    def __turns(self):
        self.program += "%% possible turns\n"
        for turn_no in range(1, self.max_turns + 1):
            player = "x" if turn_no % 2 == 1 else "o"
            self.program += "turn(" + player + "," + str(turn_no) + ").\n"
        self.program += "\n"

    def __board(self):
        self.program += "%% board\n"
        self.program += "board(" + ",".join("n" * (self.grid_size ** 2)) + ",0).\n\n" 

    def __moves(self):
        self.program += "%% moves\n"
        for i in range(1, self.grid_size ** 2 + 1):
            before = ",".join(["S" + str(j) for j in range(1, i)]) + "," if i > 1 else "" # cells before Si
            after = "," + ",".join(["S" + str(k) for k in range(i+1, self.grid_size ** 2 + 1)]) if i < self.grid_size ** 2 else "" # cells after Si
            prev_board = "board({prev}n{succ},A)".format(prev = before, succ = after) # the state of the board prior to the move
            next_board_x = "board({prev}x{succ},B)".format(prev = before, succ = after)
            next_board_o = "board({prev}o{succ},B)".format(prev = before, succ = after)
            next_board_n = "board({prev}n{succ},B)".format(prev = before, succ = after)
            x_good = "{next_state} :- {last_state}, turn(x,B), square{no}good(B), B is A+1.\n".format(next_state = next_board_x, last_state = prev_board, no = str(i))
            o_good = "{next_state} :- {last_state}, turn(o,B), square{no}good(B), B is A+1.\n".format(next_state = next_board_o, last_state = prev_board, no = str(i))
            x_bad = "{next_state} :- {last_state}, turn(x,B), square{no}bad(B), B is A+1.\n".format(next_state = next_board_o, last_state = prev_board, no = str(i))
            o_bad = "{next_state} :- {last_state}, turn(o,B), square{no}bad(B), B is A+1.\n".format(next_state = next_board_x, last_state = prev_board, no = str(i))
            neutral = "{next_state} :- {last_state}, turn(_,B), square{no}neutral(B), B is A+1.\n".format(next_state = next_board_n, last_state = prev_board, no = str(i))
            self.program = self.program + x_good + o_good + x_bad + o_bad + neutral
        self.program += "\n"     

    def __win_condition(self): # only defined for grid sizes up to 3, since this is what we are gonna use anyway
        self.program += "%% win conditions\n"
        if self.grid_size == 1:
            self.program += "win(B) :- board(x,B).\n\n"
        elif self.grid_size == 2: # exclude diagonals for a more fair game
            self.program += "win(B) :- board(x,x,_,_,B); board(x,_,x,_,B); board(_,x,_,x,B).\n\n"
        elif self.grid_size == 3:
            self.program = (self.program + "win(B) :- board(x,x,x,S4,S5,S6,S7,S8,S9,B).\n"
            + "win(B) :- board(S1,S2,S3,x,x,x,S7,S8,S9,B).\n"
            + "win(B) :- board(S1,S2,S3,S4,S5,S6,x,x,x,B).\n"
            + "win(B) :- board(x,S2,S3,x,S5,S6,x,S8,S9,B).\n"
            + "win(B) :- board(S1,x,S3,S4,x,S6,S7,x,S9,B).\n"
            + "win(B) :- board(S1,S2,x,S4,S5,x,S7,S8,x,B).\n"
            + "win(B) :- board(x,S2,S3,S4,x,S6,S7,S8,x,B).\n"
            + "win(B) :- board(x,S2,S3,S4,x,S6,S7,S8,x,B).\n\n"
            )
        else:
            raise Exception("Win condition undefined for grid sizes > 3. Sorry!")

    def __lose_condition(self): # only defined for grid sizes up to 3, since this is what we are gonna use anyway
        self.program += "%% lose conditions\n"
        if self.grid_size == 1:
            self.program += "lose(B) :- board(o,B).\n\n"
        elif self.grid_size == 2:
            self.program += "lose(B) :- board(o,o,_,_,B); board(o,_,o,_,B); board(_,o,_,o,B).\n\n"
        elif self.grid_size == 3:
            self.program = (self.program + "lose(B) :- board(o,o,o,S4,S5,S6,S7,S8,S9,B).\n"
            + "lose(B) :- board(S1,S2,S3,o,o,o,S7,S8,S9,B).\n"
            + "lose(B) :- board(S1,S2,S3,S4,S5,S6,o,o,o,B).\n"
            + "lose(B) :- board(o,S2,S3,o,S5,S6,o,S8,S9,B).\n"
            + "lose(B) :- board(S1,o,S3,S4,o,S6,S7,o,S9,B).\n"
            + "lose(B) :- board(S1,S2,o,S4,S5,o,S7,S8,o,B).\n"
            + "lose(B) :- board(o,S2,S3,S4,o,S6,S7,S8,o,B).\n"
            + "lose(B) :- board(o,S2,S3,S4,o,S6,S7,S8,o,B).\n"
            )
        else:
            raise Exception("Lose condition undefined for grid sizes > 3. Sorry!")
        


    
class Strategy:
    pass


class Test:
    pass

if __name__ == "__main__": 
    game = ProbTicTacToe(grid_size=2)
    # print(get_evaluatable().create_from(game.problog_program).evaluate())
    # print(game.program)
    print(game.query("win(2)"))