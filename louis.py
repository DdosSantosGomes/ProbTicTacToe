"""
The code in this file is the work of Louis Abraham 
and taken from his blogpost at https://louisabraham.github.io/articles/probabilistic-tic-tac-toe. 
One function has been slightly modified.
"""

import random
from functools import lru_cache

def hull_intersection(f, g):
    """
    f and g are two lists of tuples (a, b) representing linear functions
    solves
    y = max_i f_i(x)
    x = min_i g_i(y)

    Also returns the indices of the optimal functions.

    This is the work of Louis Abahram 
    (see: https://louisabraham.github.io/articles/probabilistic-tic-tac-toe)
    """
    a, b = 0, 1
    while b - a > 1e-9:
        x = (a + b) / 2
        y = max(a * x + b for a, b in f)
        x1 = min(a * y + b for a, b in g)
        if x1 < x:
            b = x
        else:
            a = x
    x = (a + b) / 2
    y, i = max((a * x + b, i) for i, (a, b) in enumerate(f))
    x, j = min((a * y + b, i) for i, (a, b) in enumerate(g))
    return (y, i), (x, j)

def generate_cell():
    """ This is the work of Louis Abahram (see: https://louisabraham.github.io/articles/probabilistic-tic-tac-toe) """
    neutral = random.choice(range(5, 35, 5))
    success = random.choice(range(30, 100 - neutral + 5, 5))
    failure = 100 - neutral - success
    return success / 100, neutral / 100, failure / 100

def generate_grid():
    """ This is the work of Louis Abahram (see: https://louisabraham.github.io/articles/probabilistic-tic-tac-toe) """
    return tuple(generate_cell() for _ in range(9))

def apply(state, cell, player):
    """ This is the work of Louis Abahram (see: https://louisabraham.github.io/articles/probabilistic-tic-tac-toe) """
    return tuple(player if i == cell else v for i, v in enumerate(state))


def winner(state): 
    """ This is the work of Louis Abahram (see: https://louisabraham.github.io/articles/probabilistic-tic-tac-toe).
    This function is slightly modified to return "t" in case of a tie. """
    for i in range(3):
        if state[i] == state[i + 3] == state[i + 6] and state[i] is not None:
            return state[i]
        if (
            state[3 * i] == state[3 * i + 1] == state[3 * i + 2]
            and state[3 * i] is not None
        ):
            return state[3 * i]
    if state[0] == state[4] == state[8] and state[0] is not None:
        return state[0]
    if state[2] == state[4] == state[6] and state[2] is not None:
        return state[2]
    if available_cells(state) == []:
        return "t"
    return None

def available_cells(state):
    """ This is the work of Louis Abahram (see: https://louisabraham.github.io/articles/probabilistic-tic-tac-toe) """
    return [i for i, v in enumerate(state) if v is None]

@lru_cache(3**9)
def value(grid, state=(None,) * 9):
    """
    Returns V(s) and V'(s) along with the optimal actions.

    This is the work of Louis Abahram (see: https://louisabraham.github.io/articles/probabilistic-tic-tac-toe).
    """
    w = winner(state)
    if w == "x":
        return (1, None), (1, None)
    elif w == "o":
        return (0, None), (0, None)

    cells = available_cells(state)
    if not cells:
        return (0.5, None), (0.5, None)

    f = []
    g = []
    for cell in cells:
        success, neutral, failure = grid[cell]
        s1 = apply(state, cell, "x")
        (v1, _), (vp1, _) = value(grid, s1)
        s2 = apply(state, cell, "o")
        (v2, _), (vp2, _) = value(grid, s2)
        x_c = success * vp1 + failure * vp2
        xp_c = success * v2 + failure * v1
        f.append((neutral, x_c))
        g.append((neutral, xp_c))
    (v, i), (vp, ip) = hull_intersection(f, g)
    return (v, cells[i]), (vp, cells[ip])