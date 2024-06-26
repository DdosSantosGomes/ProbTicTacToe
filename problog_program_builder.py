import textwrap

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
            # print(self._get_program())
            problog_program = PrologString(self._get_program())
            result = get_evaluatable().create_from(problog_program).evaluate()
        except:
            raise ProbLogRuntimeException('The query {} cannot be computed'.format(query))
        return list(result.values())[0]
    
    def update_board(self, new_board):
        """ Input new_board as a list of facts of the form `board(cell_nr, mark, 0)`. """
        self._program['board'] = ''
        for cell_state in new_board:
            self._program['board'] += cell_state

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
        good = clause(
            head = function(BOARD, variable(C), variable(P), variable(B)),
            body = term_conj(
                function(BOARD, variable(C), constant(N), variable(A)),
                function(CELL, variable(C), constant(GOOD), variable(B)),
                function(TURN, variable(P), variable(B)),
                function(PLAY, variable(C), variable(B))
            ),
            constraint = simple_constraint(variable(B), variable(A))
        )
        x_bad = clause(
            head = function(BOARD, variable(C), constant(O), variable(B)),
            body = term_conj(
                function(BOARD, variable(C), constant(N), variable(A)),
                function(CELL, variable(C), constant(BAD), variable(B)),
                function(TURN, constant(X), variable(B)),
                function(PLAY, variable(C), variable(B))
            ),
            constraint = simple_constraint(variable(B), variable(A))
        )
        o_bad = clause(
            head = function(BOARD, variable(C), constant(X), variable(B)),
            body = term_conj(
                function(BOARD, variable(C), constant(N), variable(A)),
                function(CELL, variable(C), constant(BAD), variable(B)),
                function(TURN, constant(O), variable(B)),
                function(PLAY, variable(C), variable(B))
            ),
            constraint = simple_constraint(variable(B), variable(A))
        )
        neutral = clause(
            head = function(BOARD, variable(C), constant(N), variable(B)),
            body = term_conj(
                function(BOARD, variable(C), constant(N), variable(A)),
                function(CELL, variable(C), constant(GOOD), variable(B)),
                function(TURN, ANY, variable(B)),
                function(PLAY, variable(C), variable(B))
            ),
            constraint = simple_constraint(variable(B), variable(A))
        )
        unchanged = clause(
            head = function(BOARD, variable(C), variable(P), variable(B)),
            body = term_conj(
                function(BOARD, variable(C), variable(P), variable(A)),
                function(TURN, ANY, variable(B)),
                negate(function(PLAY, variable(C), variable(B)))
            ),
            constraint = simple_constraint(variable(B), variable(A))
        )
        self._program['moves'] = self._program['moves'] + good + x_bad + o_bad + neutral + unchanged

    def _end_conditions(self):
        self._program['end_conditions'] = textwrap.dedent("""
            win1(A) :- board(1,x,A),board(2,x,A),board(3,x,A).
            win2(A) :- board(4,x,A),board(5,x,A),board(6,x,A).
            win3(A) :- board(7,x,A),board(8,x,A),board(9,x,A).
            win4(A) :- board(1,x,A),board(4,x,A),board(7,x,A).
            win5(A) :- board(2,x,A),board(5,x,A),board(8,x,A).
            win6(A) :- board(3,x,A),board(6,x,A),board(9,x,A).
            win7(A) :- board(3,x,A),board(5,x,A),board(7,x,A).
            win8(A) :- board(1,x,A),board(5,x,A),board(9,x,A).

            lose1(A) :- board(1,o,A),board(2,o,A),board(3,o,A).
            lose2(A) :- board(4,o,A),board(5,o,A),board(6,o,A).
            lose3(A) :- board(7,o,A),board(8,o,A),board(9,o,A).
            lose4(A) :- board(1,o,A),board(4,o,A),board(7,o,A).
            lose5(A) :- board(2,o,A),board(5,o,A),board(8,o,A).
            lose6(A) :- board(3,o,A),board(6,o,A),board(9,o,A).
            lose7(A) :- board(3,o,A),board(5,o,A),board(7,o,A).
            lose8(A) :- board(1,o,A),board(5,o,A),board(9,o,A).
                                                          
            win(A) :- win1(A) ; win2(A) ; win3(A) ; win4(A); win5(A) ; win6(A) ; win7(A) ; win8(A).
            lose(A) :- lose1(A) ; lose2(A) ; lose3(A) ; lose4(A); lose5(A) ; lose6(A) ; lose7(A) ; lose8(A).
                                                          
            win(B) :- win(A), turn(_,B), B is A+1.
            lose(B) :- lose(A), turn(_,B), B is A+1.
        """)


class ConditionUndefinedException(Exception):
    pass

class ProbLogRuntimeException(Exception):
    pass

if __name__ == "__main__": 
    # game = ProbLogProgram(None)
    # print(game._get_program())
    pass