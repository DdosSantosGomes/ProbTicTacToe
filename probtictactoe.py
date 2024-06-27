import argparse
import multiprocess as mp

from game import Game
from names import E
from strategies_aggressive import *
from strategies_defensive import *


parser = argparse.ArgumentParser(prog = 'python3 probtictactoe.py',
                                description = 'Run instances of Probabilistic Tic-Tac-Toe. \
                                    We recommend redirecting the output to a file.',
                                epilog = 'default: run 10 instances with WinFast against random, takes a few minutes'
                                )

parser.add_argument('--nr_games', type = int, nargs = 1,
                    help = 'number of instances to run',
                    metavar = 'N',
                    default = 10,
                    required = False,
                    dest = 'nr_games'
                    )

parser.add_argument('--strategy', type = str, nargs = 1,
                    choices = ['WF', 'CBA', 'TF', 'CBD'],
                    help = 'specific strategy you want to see in action',
                    default = 'WF',
                    required = False,
                    dest = 'strategy'
                    )

parser.add_argument('--opposing_strategy', type = str, nargs = 1,
                    choices = ['optimal', 'random'],
                    help = 'specific strategy you want to play against',
                    default = 'random',
                    required = False,
                    dest = 'opposing_strategy'
                    )

parser.add_argument('--all', type = bool, nargs = 1,
                    help = 'run 1000 simulations for each strategy against both optimal and random,\
                        note that this might take hours, \
                        and it also basically overrides all other arguments',
                    metavar = '{True,False}',
                    default = False,
                    required = False,
                    dest = 'all'
                    )

args = parser.parse_args()

nr_games = args.nr_games[0]
strategy = args.strategy
if strategy == 'WF':
    strategy = WinFast
elif strategy == 'CBA':
    strategy = ConquerBoardAggressive
elif strategy == 'TF':
    strategy = TieFast
elif strategy == 'CBD':
    strategy = ConquerBoardDefensive
opposing_strategy = args.opposing_strategy
all = args.all

if not all: 
    Game(games = nr_games, opposing = opposing_strategy).simulate(E, strategy)
if all:
    ## playing our strategies against LOUIS
    wf_v_louis = mp.Process(target=Game(games=nr_games,opposing='louis').simulate, args=(E,WinFast))
    cba_v_louis = mp.Process(target=Game(games=nr_games,opposing='louis').simulate, args=(E,ConquerBoardAggressive))
    tf_v_louis = mp.Process(target=Game(games=nr_games,opposing='louis').simulate, args=(E,TieFast))
    cbd_v_louis = mp.Process(target=Game(games=nr_games,opposing='louis').simulate, args=(E,ConquerBoardDefensive))

    ## playing our strategies against RANDOM
    wf_v_rand = mp.Process(target=Game(games=nr_games,opposing='random').simulate, args=(E,WinFast))
    cba_v_rand = mp.Process(target=Game(games=nr_games,opposing='random').simulate, args=(E,ConquerBoardAggressive))
    tf_v_rand = mp.Process(target=Game(games=nr_games,opposing='random').simulate, args=(E,TieFast))
    cbd_v_rand = mp.Process(target=Game(games=nr_games,opposing='random').simulate, args=(E,ConquerBoardDefensive))

    wf_v_louis.start()
    cba_v_louis.start()
    tf_v_louis.start()
    cbd_v_louis.start()
    wf_v_rand.start()
    cba_v_rand.start()
    tf_v_rand.start()
    cbd_v_rand.start()
