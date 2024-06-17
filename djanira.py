import random

from problog import get_evaluatable
from problog.program import SimpleProgram
from problog.logic import Constant,Var,Term,AnnotatedDisjunction

# How to get this to work: 
# In vscode search bar: type ">" and search for "Python: Create Environment"
# Now create environment and inside it, run "python3 -m pip install problog" in vscode terminal 
# Now the environment and problog are installed in your tictactoe map 
# Running the file looks like this for me:     
# (.venv) Airvanlcaladmin:ProbTicTacToe djanira$ python3 djanira.py


# Random probability distribution and grid generator 
# Based on Louis Abraham's definitions 
def generate_cell():
    neutral = random.choice(range(5, 35, 5))
    success = random.choice(range(30, 100 - neutral + 5, 5))
    failure = 100 - neutral - success
    return success / 100, failure / 100, neutral / 100

def generate_grid():
    return tuple(generate_cell() for _ in range(9))

probs = generate_grid() 

# Example from tutorial: this works 
# coin,heads,tails,win,query = Term('coin'),Term('heads'),Term('tails'),Term('win'),Term('query')
# C = Var('C')
# p = SimpleProgram()
# p += coin(Constant('c1'))
# p += coin(Constant('c2'))
# p += AnnotatedDisjunction([heads(C,p=0.4), tails(C,p=0.6)], coin(C))
# p += (win << heads(C))
# p += query(win)


# Initializing terms and variables of the Problog program
mark, cell, board = Term('mark'), Term('cell'), Term('board')
G, B, N = Term('G'), Term('B'), Term('N')

x = Constant('x')
o = Constant('o')
n = Constant('n')

for i in range(9):
    ci = Constant(str(i))

turn = Term('turn')
query = Term('query')

p = SimpleProgram()

# Marks, cells, and initial state of board
p += mark(x)
p += mark(o)
p += mark(n)

for i in range(9):
    p += cell(ci) 

p += board(n,n,n,n,n,n,n,n,n)

# Turns
for i in range(9):
    p += turn(i)

# Probability distributions for each cell
# This gives an error still: TypeError: AnnotatedDisjunction.__init__() missing 1 required positional argument: 'body'
for i in range(9):
    (good, bad, neutral) = probs[i] 
    s = str(i)
    p += AnnotatedDisjunction([G(s,p=good), 
                               B(s,p=bad),
                               N(s,p=neutral)])
    
# Calculating next moves: Missing 

# Defining winning and losing: Missing
    
# Queries: Missing

# p += (win << heads(C))
# p += query(win)


val = get_evaluatable().create_from(p).evaluate()

print(probs)
print(val)