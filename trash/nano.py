import random

from problog import get_evaluatable
from problog.program import PrologString

from problog_program_syntax import *

# term names, centralized
SQUARE_GOOD = 'square_good'
SQUARE_NEUTRAL = 'square_neutral'
SQUARE_BAD = 'square_bad'
TURN = 'turn'
BOARD = 'board'
CHOOSE = 'choose'
WIN = 'win'
LOSE = 'lose'
A = 'A'
B = 'B'
ANY = '_'

class ProbTicTacToe:
    """
    Objects of this class are instances of a game of ProbTicTacToe.
    """


    program = {}
    """
    This is a dictionary indexed by the sections of our ProbLog program.
    In particular, our indices are:
        - board
        - grid
        - turns
        - moves
        - win
        - lose \n
    and they correspond to the fixed game logic of the game of ProbTicTacToe. \n
    This is an internal representation which should be kept hidden.
    """

    def __init__(self, grid_size = 3, max_turns = None): 
        self.grid_size = grid_size
        self.max_turns = self.grid_size ** 2 + 1 if max_turns is None else max_turns
        self.grid = self.__generate_grid()
        self.__build_program()

    def get_program(self):
        program = ''
        for prog in self.program.values():
            program += prog
            program += '\n'
        return program

    def __build_program(self):
        self.__init_board()
        self.__grid()
        self.__turns()
        # self.__choose()
        self.__moves()
        self.__win_condition()
        self.__lose_condition()

    def run(self, strategy): # Test a single game with a given strategy against the AI
        pass

    def query(self, *queries):
        """
        
        """
        results = {}
        program = ''
        for prog in self.program.values():
            program += prog
        for query in queries:
            query_str = 'query({q}).'.format(q = query)
            try:
                result = get_evaluatable().create_from(PrologString(program + query_str)).evaluate()
            except:
                raise Exception(query + ' is not valid Prolog!')
            results.update(result)
        return results

    def __generate_grid(self):
        def generate_square():
            neutral = random.choice(range(5, 35, 5))
            success = random.choice(range(30, 100 - neutral + 5, 5))
            failure = 100 - neutral - success
            return success / 100, neutral / 100, failure / 100
        return tuple(generate_square() for _ in range(self.grid_size ** 2))
    
    def __grid(self):
        self.program['grid'] = ''
        for cell_no in range(self.grid_size ** 2):
            current_cell = self.grid[cell_no]
            p_good = current_cell[0]
            a1 = probabilistic_fact(p_good, function(SQUARE_GOOD, cell_no+1, variable(A)))
            p_neutral = current_cell[1]
            a2 = probabilistic_fact(p_neutral, function(SQUARE_NEUTRAL, cell_no+1, variable(A)))
            p_bad = current_cell[2]
            a3 = probabilistic_fact(p_bad, function(SQUARE_BAD, cell_no+1, variable(A)))
            self.program['grid'] += annotated_disjunction_with_body( 
                annotated_disj = annotated_disjunction(a1, a2, a3),
                body = function(TURN, ANY, variable(A))
            )

    def __turns(self):
        self.program['turns'] = ''
        for turn_no in range(1, self.max_turns + 1):
            player = "x" if turn_no % 2 == 1 else "o"
            self.program['turns'] += fact(function(TURN, player, turn_no))

    def __init_board(self):
        self.program['start_board'] = fact(function(BOARD, *(('n',) * (self.grid_size ** 2) + (0,)) ))

    # def __choose(self):
    #     self.program += '%% available positions\n'
    #     choose_all, chosen = '', ''
    #     for cell_no in range(1, self.grid_size ** 2 + 1):
    #         choose_all += clause(
    #             head = function(self.CHOOSE, cell_no, 'B'),
    #             body = conj(
    #                 function(self.CHOOSE, cell_no, 'A'),
    #                 function(self.SQUARE_NEUTRAL, cell_no, 'B'),
    #                 function(self.TURN, '_', 'B')
    #             ),
    #             constraint = 'B is A+1'
    #         )
    #         # is_available_start += fact(function(self.CHOOSE, cell_no, 0))
    #         chosen += clause(
    #             head = function(self.CHOOSE, cell_no, 'B'),
    #             body = conj(
                    
    #             ),
    #             constraint = 'B is A+1'
    #         )
    #     self.program += choose_all
    #     self.program += chosen
    #     self.program += '\n'

    def __moves(self):
        self.program['moves'] = ''
        for cell_no in range(1, self.grid_size ** 2 + 1):
            before = ['S' + str(j) for j in range(1, cell_no)]
            after = ['S' + str(k) for k in range(cell_no+1, self.grid_size ** 2 + 1)]

            prev_board = function(BOARD, *(before + ['n'] + after + [variable(A)]))
            next_board_x = function(BOARD, *(before + ['x'] + after + [variable(B)]))
            next_board_o = function(BOARD, *(before + ['o'] + after + [variable(B)]))
            next_board_n = function(BOARD, *(before + ['n'] + after + [variable(B)]))

            x_good = clause(
                head = next_board_x,
                body = conj(
                    prev_board, function(TURN, 'x', variable(B)), function(SQUARE_GOOD, cell_no, variable(B)), function(CHOOSE, cell_no, variable(A))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            o_good = clause(
                head = next_board_o,
                body = conj(
                    prev_board, function(TURN, 'o', variable(B)), function(SQUARE_GOOD, cell_no, variable(B)), function(CHOOSE, cell_no, variable(A))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            x_bad = clause(
                head = next_board_x,
                body = conj(
                    prev_board, function(TURN, 'o', variable(B)), function(SQUARE_BAD, cell_no, variable(B)), function(CHOOSE, cell_no, variable(A))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            o_bad = clause(
                head = next_board_o,
                body = conj(
                    prev_board, function(TURN, 'x', variable(B)), function(SQUARE_BAD, cell_no, variable(B)), function(CHOOSE, cell_no, variable(A))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            neutral = clause(
                head = next_board_n,
                body = conj(
                    prev_board, function(TURN, ANY, variable(B)), function(SQUARE_NEUTRAL, cell_no, variable(B)), function(CHOOSE, cell_no, variable(A))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            self.program['moves'] = self.program['moves'] + x_good + o_good + x_bad + o_bad + neutral

    def __win_condition(self): # only defined for grid sizes up to 3, since this is what we are gonna use anyway
        if self.grid_size == 1:
            self.program['win'] = "win(B) :- board(x,B).\n\n"
        elif self.grid_size == 2: # exclude diagonals for a more fair game
            self.program['win'] = "win(B) :- board(x,x,_,_,B); board(x,_,x,_,B); board(_,x,_,x,B).\n\n"
        elif self.grid_size == 3:
            self.program['win'] = ("win(B) :- board(x,x,x,S4,S5,S6,S7,S8,S9,B).\n"
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
        if self.grid_size == 1:
            self.program['lose'] = "lose(B) :- board(o,B).\n\n"
        elif self.grid_size == 2:
            self.program['lose'] = "lose(B) :- board(o,o,_,_,B); board(o,_,o,_,B); board(_,o,_,o,B).\n\n"
        elif self.grid_size == 3:
            self.program['lose'] = ("lose(B) :- board(o,o,o,S4,S5,S6,S7,S8,S9,B).\n"
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
        

def pretty(d):
    for value in d.values():
        print(str(value))

if __name__ == "__main__": 
    game = ProbTicTacToe(grid_size=3)
    print(game.get_program())
    # print(get_evaluatable().create_from(game.problog_program).evaluate())
    # print(game.program.values())
    # print(game.query("win(1)","win(3)"))
    # print(game.program)