# Probabilistic Tic-Tac-Toe in ProbLog (and Python)

Probabilistic Tic-Tac-Toe is an online game developed by [Cameron Sun](https://www.csun.io/2024/06/08/probabilistic-tic-tac-toe.html). An optimal solution exists, and was discovered by [Louis Abraham](https://louisabraham.github.io/articles/probabilistic-tic-tac-toe). ProbLog is a probabilistic logic programming language developed at [KU Leuven](https://dtai.cs.kuleuven.be/problog/). In this project, we model Probabilistic Tic-Tac-Toe in ProbLog, and we implement strategies that we test against the optimal one or a random agent.

Some code is borrowed from Louis Abraham (see his blogpost [here](https://louisabraham.github.io/articles/probabilistic-tic-tac-toe)) - this is made explicit wherever relevant.

## Setup

### Short version

Requires `problog` (which might also require `setuptools`) and `multiprocess`. You might want to do this in a virtual environment. Please use Python 3.12.

### Longer version

You need to install the Python `problog` package from [here](https://dtai.cs.kuleuven.be/problog/tutorial/advanced/01_python_interface.html). Since our ProbLog program is very slow, we tried to speed it up via multi-threading - you therefore also need the package `multiprocess`. Note that it is still quite slow (though at least usable) as simulating even only 30 games takes around 15 minutes (on an M1 MacBook).

On our (Apple Silicon) MacBooks, we had to create it in a virtual environment and run our code in it. 
This is how we did it: 
  - `python3 -m venv ~/.venv` in the root directory
  - `source ~/.venv/bin/activate`
  - actually run the program, with `python3 game.py` - we also redirected the output to `output.txt`
  - `deactivate` to exit the virtual environment

Please use Python 3.12.

## Possible issues!

We are all running Apple Silicon MacBooks (M1 and M2), so maybe this is only relevant to people using similar machines. On an M1 MacBook, we ran into a `ModuleNotFoundError: No module named 'distutils'` whenever we tried to run the program more than once - to solve this, we found out that it (mostly) worked to uninstall the package `setuptools`, and then reinstall it again. 
This is definitely not an ideal solution, but we did not dig deeper into this as we could still run the program easily on another machine.
