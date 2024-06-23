from math import sqrt
import random

from problog import get_evaluatable
from problog.program import PrologString

from problog_utils import *
from names import *


class ProbLogProgram:
    """
    Objects of this class are ProbLog programs that model a state of the game of ProbTicTacToe.\n
    They support queries about the probability of winning or losing from the given state, 
    if certains moves are made and that can also be updated with evidence, with a lookahead of three turns.
    """

    _program = {}
    """
    This is an internal representation which should be kept hidden. \n
    It is a dictionary indexed by the sections of our ProbLog program.
    In particular, our indices are:
        - board (current state of the board)
        - grid (fixed board)
        - turns (who plays when)
        - moves (legal move predicate)
        - win (winning condition)
        - lose (losing condition)
        - play (uniform probability distribution of the candidate cells to play, fed by the strategies)
        - (possibly) queries
        - (possibly) evidence \n
    and they correspond to the fixed game logic of the game of ProbTicTacToe.
    """
    
    def __init__(self, grid): 
        self.grid = self._generate_grid() if grid is None else grid
        self._init_board()
        self._grid()
        self._init_turns()
        self._moves()
        self._win_condition()
        self._lose_condition()

    def _get_program(self):
        program = ''
        for index,prog in self._program.items():
            if index == 'queries' or index == 'evidence':
                continue
            program += prog
        # make sure that we add evidence and then queries at the end of the program
        if 'evidence' in self._program.keys():
            program += self._program['evidence']
        if 'queries' in self._program.keys():
            program += self._program['queries']
        return program

    def query(self, *queries, evidence = None):
        """
        Use in combination with utils.query and utils.evidence to generate syntactically valid ProbLog queries.
        """
        self._program['queries'] = ''
        for query in queries:
            self._program['queries'] += query
        try:
            if evidence is not None:
                self._program['evidence'] = evidence
            problog_program = PrologString(self._get_program())
            result = get_evaluatable().create_from(problog_program).evaluate()
        except:
            raise ProbLogRuntimeException('The queries {} cannot be computed'
                                          .format(', '.join( [q[:-2] for q in queries] ))
                                          )
        return result
    
    def update_board(self, new_board):
        self._program['board'] = new_board

    def update_win_conditions(self, *conditions):
        for condition in conditions: 
            self._program['win'] += condition

    def update_lose_conditions(self, *conditions):
        for condition in conditions: 
            self._program['lose'] += condition

    def update_play(self, prob_dist):
        self._program['play'] = prob_dist
    
    def _grid(self):
        self._program['grid'] = ''
        for cell_no in range(len(self.grid)):
            current_cell = self.grid[cell_no]
            p_good, p_neutral, p_bad = current_cell[0], current_cell[1], current_cell[2]
            a1 = probabilistic_fact(p_good, 
                                    function(SQUARE_GOOD, constant(cell_no+1), variable(A))
                                    )
            a2 = probabilistic_fact(p_neutral, 
                                    function(SQUARE_NEUTRAL, constant(cell_no+1), variable(A))
                                    )
            a3 = probabilistic_fact(p_bad, 
                                    function(SQUARE_BAD, constant(cell_no+1), variable(A))
                                    )
            self._program['grid'] += annotated_disjunction_with_body( 
                annotated_disj = annotated_disjunction(a1, a2, a3),
                body = function(TURN, ANY, variable(A))
            )

    def _init_turns(self):
        self._program['turns'] = ''
        for turn_no in range(1, 4): # we only look 3 turns ahead
            player = "x" if turn_no % 2 == 1 else "o"
            self._program['turns'] += fact(function(TURN, constant(player), constant(turn_no)))

    def _init_board(self):
        initial_config = (N,) * (len(self.grid)) + (0,)
        self._program['start_board'] = fact(
            function(
                BOARD, 
                *[ constant(x) for x in initial_config ]
                )
            )

    def _moves(self):
        self._program['moves'] = ''
        for cell_no in range(1, len(self.grid) + 1):
            before = ['S' + str(j) for j in range(1, cell_no)]
            after = ['S' + str(k) for k in range(cell_no+1, len(self.grid)+1)]
            before, after = [variable(x) for x in before], [variable(x) for x in after]

            prev_board = function(
                BOARD, *(before + [constant(N)] + after + [variable(A)])
                )
            next_board_x = function(
                BOARD, *(before + [constant(X)] + after + [variable(B)])
                )
            next_board_o = function(
                BOARD, *(before + [constant(O)] + after + [variable(B)])
                )
            next_board_n = function(
                BOARD, *(before + [constant(N)] + after + [variable(B)])
                )

            x_good = clause(
                head = next_board_x,
                body = term_conj(
                    prev_board, 
                    function(TURN, constant(X), variable(B)), 
                    function(SQUARE_GOOD, constant(cell_no), variable(B))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            o_good = clause(
                head = next_board_o,
                body = term_conj(
                    prev_board, 
                    function(TURN, constant(O), variable(B)), 
                    function(SQUARE_GOOD, constant(cell_no), variable(B))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            x_bad = clause(
                head = next_board_x,
                body = term_conj(
                    prev_board, 
                    function(TURN, constant(O), variable(B)), 
                    function(SQUARE_BAD, constant(cell_no), variable(B))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            o_bad = clause(
                head = next_board_o,
                body = term_conj(
                    prev_board, 
                    function(TURN, constant(X), variable(B)), 
                    function(SQUARE_BAD, constant(cell_no), variable(B))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            neutral = clause(
                head = next_board_n,
                body = term_conj(
                    prev_board, 
                    function(TURN, ANY, variable(B)), 
                    function(SQUARE_NEUTRAL, constant(cell_no), variable(B))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            self._program['moves'] = self._program['moves'] + x_good + o_good + x_bad + o_bad + neutral

    def _win_condition(self): # only defined for grid sizes up to 3, since this is what we are gonna use anyway
        size = int(sqrt(len(self.grid)))
        if size == 1:
            self._program['win'] = "win(B) :- board(x,B).\n\n"
        elif size == 2: # exclude diagonals for a more fair game
            self._program['win'] = "win(B) :- board(x,x,_,_,B); board(x,_,x,_,B); board(_,x,_,x,B).\n\n"
        elif size == 3:
            self._program['win'] = ("win1(B) :- board(x,x,x,S4,S5,S6,S7,S8,S9,B).\n"
            + "win1(B) :- win1(A), B is A+1.\n"
            + "win2(B) :- board(S1,S2,S3,x,x,x,S7,S8,S9,B).\n"
            + "win2(B) :- win2(A), B is A+1.\n"
            + "win3(B) :- board(S1,S2,S3,S4,S5,S6,x,x,x,B).\n"
            + "win3(B) :- win3(A), B is A+1.\n"
            + "win4(B) :- board(x,S2,S3,x,S5,S6,x,S8,S9,B).\n"
            + "win4(B) :- win4(A), B is A+1.\n"
            + "win5(B) :- board(S1,x,S3,S4,x,S6,S7,x,S9,B).\n"
            + "win5(B) :- win5(A), B is A+1.\n"
            + "win6(B) :- board(S1,S2,x,S4,S5,x,S7,S8,x,B).\n"
            + "win6(B) :- win6(A), B is A+1.\n"
            + "win7(B) :- board(x,S2,S3,S4,x,S6,S7,S8,x,B).\n"
            + "win7(B) :- win7(A), B is A+1.\n"
            + "win8(B) :- board(x,S2,S3,S4,x,S6,S7,S8,x,B).\n"
            + "win8(B) :- win8(A), B is A+1.\n"
            )
        else:
            raise ConditionUndefinedException("Win condition undefined for grid sizes > 3. Sorry!")

    def _lose_condition(self): # only defined for grid sizes up to 3, since this is what we are gonna use anyway
        size = int(sqrt(len(self.grid)))
        if size == 1:
            self._program['lose'] = "lose(B) :- board(o,B).\n\n"
        elif size == 2:
            self._program['lose'] = "lose(B) :- board(o,o,_,_,B); board(o,_,o,_,B); board(_,o,_,o,B).\n\n"
        elif size == 3:
            self._program['lose'] = ("lose1(B) :- board(o,o,o,S4,S5,S6,S7,S8,S9,B).\n"
            + "lose1(B) :- lose1(A), B is A+1.\n"
            + "lose2(B) :- board(S1,S2,S3,o,o,o,S7,S8,S9,B).\n"
            + "lose2(B) :- lose2(A), B is A+1.\n"
            + "lose3(B) :- board(S1,S2,S3,S4,S5,S6,o,o,o,B).\n"
            + "lose3(B) :- lose3(A), B is A+1.\n"
            + "lose4(B) :- board(o,S2,S3,o,S5,S6,o,S8,S9,B).\n"
            + "lose4(B) :- lose4(A), B is A+1.\n"
            + "lose5(B) :- board(S1,o,S3,S4,o,S6,S7,o,S9,B).\n"
            + "lose5(B) :- lose5(A), B is A+1.\n"
            + "lose6(B) :- board(S1,S2,o,S4,S5,o,S7,S8,o,B).\n"
            + "lose6(B) :- lose6(A), B is A+1.\n"
            + "lose7(B) :- board(o,S2,S3,S4,o,S6,S7,S8,o,B).\n"
            + "lose7(B) :- lose7(A), B is A+1.\n"
            + "lose8(B) :- board(S1,S2,o,S4,o,S6,o,S8,S9,B).\n"
            + "lose8(B) :- lose8(A), B is A+1.\n"
            )
        else:
            raise ConditionUndefinedException("Lose condition undefined for grid sizes > 3. Sorry!")
        
    # only for testing. Based on Louis Abraham's work
    def _generate_grid(self):
        def generate_square():
            neutral = random.choice(range(5, 35, 5))
            success = random.choice(range(30, 100 - neutral + 5, 5))
            failure = 100 - neutral - success
            return success / 100, neutral / 100, failure / 100
        return tuple(generate_square() for _ in range(9))
        

class ConditionUndefinedException(Exception):
    pass

class ProbLogRuntimeException(Exception):
    pass

if __name__ == "__main__": 
    game = ProbLogProgram(None)
    print(game._get_program())