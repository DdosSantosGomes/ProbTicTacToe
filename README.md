# Probabilistic Tic-Tac-Toe in ProbLog (and Python)

Probabilistic Tic-Tac-Toe is an online game developed by [Cameron Sun](https://www.csun.io/2024/06/08/probabilistic-tic-tac-toe.html). An optimal solution exists, and was discovered by [Louis Abraham](https://louisabraham.github.io/articles/probabilistic-tic-tac-toe). ProbLog is a probabilistic logic programming language developed at [KU Leuven](https://dtai.cs.kuleuven.be/problog/). In this project, we model Probabilistic Tic-Tac-Toe in ProbLog, and we implement strategies that we test against the optimal one or a random agent.

## Setup

You need to install the Python ProbLog package from [here](https://dtai.cs.kuleuven.be/problog/tutorial/advanced/01_python_interface.html).
On our (Apple Silicon) MacBooks, this resulted in some errors, so we had to create it in a virtual environment and run our code in it. 
This is how we did it: 
  - `python3 -m venv ~/.venv` in the root directory
  - `source ~/.venv/bin/activate`
  - actually run the program, with `python3 game.py` - we also redirected the output to `output.txt`
  - `deactivate` to exit the virtual environment

Please use Python 3.12. Also note that some code is borrowed from Louis Abraham (see his blogpost [here](https://louisabraham.github.io/articles/probabilistic-tic-tac-toe)) - this is made explicit wherever relevant in our code.

## Possible issues!

We are all running Apple Silicon MacBooks (M1 and M2), so maybe this is only relevant to people using similar machines. On an M1 MacBook, we ran into a `ModuleNotFoundError: No module named 'distutils'` whenever we tried to run the program more than once - to solve this, we found out that it (mostly) worked to uninstall the package setuptools, and then reinstall it again. 
This is definitely not an ideal solution, but we did not dig deeper into this as we could still run the program easily on another machine.