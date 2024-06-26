# Probabilistic Tic-Tac-Toe in ProbLog (and Python)

Probabilistic Tic-Tac-Toe is an online game developed by [Cameron Sun](https://www.csun.io/2024/06/08/probabilistic-tic-tac-toe.html). An optimal solution exists, and was discovered by [Louis Abraham](https://louisabraham.github.io/articles/probabilistic-tic-tac-toe). ProbLog is a probabilistic logic programming language developed at [KU Leuven](https://dtai.cs.kuleuven.be/problog/). In this project, we model Probabilistic Tic-Tac-Toe in ProbLog, and we implement strategies that we test against the optimal one or a random agent.

## Setup

You need to install the Python ProbLog package from [here](https://dtai.cs.kuleuven.be/problog/tutorial/advanced/01_python_interface.html).
On our MacBooks, this resulted in some errors, so we had to create it in a virtual environment and run our code in it. 
This is how we did it: 
  - `python3 -m venv ~/.venv` in the root directory
  - `source ~/.venv/bin/activate`
  - actually run the program
  - `deactivate` to exit the virtual environment

Please use Python 3.12. Some code is borrowed from Louis Abraham (see his blogpost [here](https://louisabraham.github.io/articles/probabilistic-tic-tac-toe)). 