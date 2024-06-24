from problog import get_evaluatable
from problog.program import PrologString

from problog_utils import *
from names import *


class ProbLogProgram:
    """
    Objects of this class are ProbLog programs that model a state of the game of ProbTicTacToe.\n
    They support queries about the probability of winning or losing from the given state, 
    if certains moves are made and that can also be updated with evidence, with a default lookahead of three turns.
    """

    _program = {}
    """
    This is an internal representation which should be kept hidden. \n
    It is a dictionary indexed by the sections of our ProbLog program.
    In particular, the fixed game logic is contained in the following keys:
        - grid (fixed board)
        - turns (who plays when)
        - moves (legal move predicate)
        - end_conditions (winning or losing) \n
    while the Strategies will update these sections of the program:
        - board (current state of the board)
        - extra_end_conditions (a finer grain version of end_conditions, based on the current state)
        - play (uniform probability distribution of the candidate cells to play, fed by the strategies)
        - query
        - evidence \n
    and they correspond to the fixed game logic of the game of ProbTicTacToe.
    """
    
    def __init__(self, grid, max_turns = 3): 
        self._grid(grid)
        self._init_turns(max_turns)
        self._moves()
        self._end_conditions()

    def _get_program(self):
        program = ''
        for index,prog in self._program.items():
            if index == 'query' or index == 'evidence':
                continue
            program += prog
        # make sure that we add evidence and then queries at the end of the program
        if 'evidence' in self._program.keys():
            program += self._program['evidence']
        if 'query' in self._program.keys():
            program += self._program['query']
        return program

    def query(self, query, evidence = None):
        """ Use in combination with utils.query and utils.evidence to generate syntactically valid ProbLog queries. """
        self._program['query'] = query
        if evidence is not None:
            self._program['evidence'] = evidence
        try:
            print(self._get_program())
            problog_program = PrologString(self._get_program())
            result = get_evaluatable().create_from(problog_program).evaluate()
        except:
            raise ProbLogRuntimeException('The query {} cannot be computed'.format(query))
        return list(result.values())[0]
    
    def update_board(self, new_board):
        self._program['board'] = new_board

    def update_end_conditions(self, *conditions):
        for condition in conditions: 
            self._program['extra_end_conditions'] = condition

    def update_play(self, prob_dist):
        self._program['play'] = prob_dist
    
    def _grid(self, grid):
        self._program['grid'] = ''
        for cell_no in range(9):
            current_cell = grid[cell_no]
            p_good, p_neutral, p_bad = current_cell[0], current_cell[1], current_cell[2]
            good = probabilistic_fact(p_good, 
                                    function(CELL, constant(cell_no+1), GOOD, variable(A))
                                    )
            neutral = probabilistic_fact(p_neutral, 
                                    function(CELL, constant(cell_no+1), NEUTRAL, variable(A))
                                    )
            bad = probabilistic_fact(p_bad, 
                                    function(CELL, constant(cell_no+1), BAD, variable(A))
                                    )
            self._program['grid'] += annotated_disjunction_with_body( 
                annotated_disj = annotated_disjunction(good, neutral, bad),
                body = function(TURN, ANY, variable(A))
            )

    def _init_turns(self, max_turns):
        self._program['turns'] = ''
        for turn_no in range(1, max_turns + 1): 
            player = "x" if turn_no % 2 == 1 else "o"
            self._program['turns'] += fact(function(TURN, constant(player), constant(turn_no)))

    def _moves(self):
        self._program['moves'] = ''
        for cell_no in range(1, 10):
            before = [S + str(j) for j in range(1, cell_no)]
            after = [S + str(k) for k in range(cell_no+1, 10)]
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
                    function(CELL, constant(cell_no), GOOD, variable(B)),
                    function(PLAY, constant(cell_no), variable(B))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            o_good = clause(
                head = next_board_o,
                body = term_conj(
                    prev_board, 
                    function(TURN, constant(O), variable(B)), 
                    function(CELL, constant(cell_no), GOOD, variable(B)),
                    function(PLAY, constant(cell_no), variable(B))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            x_bad = clause(
                head = next_board_x,
                body = term_conj(
                    prev_board, 
                    function(TURN, constant(O), variable(B)), 
                    function(CELL, constant(cell_no), BAD, variable(B)),
                    function(PLAY, constant(cell_no), variable(B))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            o_bad = clause(
                head = next_board_o,
                body = term_conj(
                    prev_board, 
                    function(TURN, constant(X), variable(B)), 
                    function(CELL, constant(cell_no), BAD, variable(B)),
                    function(PLAY, constant(cell_no), variable(B))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            neutral = clause(
                head = next_board_n,
                body = term_conj(
                    prev_board, 
                    function(TURN, ANY, variable(B)), 
                    function(CELL, constant(cell_no), NEUTRAL, variable(B)),
                    function(PLAY, constant(cell_no), variable(B))
                ),
                constraint = simple_constraint(variable(B), variable(A))
            )
            self._program['moves'] = self._program['moves'] + x_good + o_good + x_bad + o_bad + neutral

    def _end_conditions(self):
        ## win conditions
        self._program['end_conditions'] = ("win1(B) :- board(x,x,x,S4,S5,S6,S7,S8,S9,B).\n"
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
        ## lose conditions
        self._program['end_conditions'] += ("lose1(B) :- board(o,o,o,S4,S5,S6,S7,S8,S9,B).\n"
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


class ConditionUndefinedException(Exception):
    pass

class ProbLogRuntimeException(Exception):
    pass

if __name__ == "__main__": 
    # game = ProbLogProgram(None)
    # print(game._get_program())
    pass