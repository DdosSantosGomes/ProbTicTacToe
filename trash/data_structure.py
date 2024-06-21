import louiswork as louiswork

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
probs = louiswork.generate_grid() 

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
mark, cell, board, win = Term('mark'), Term('cell'), Term('board'), Term('win')
G, B, N = Term('G'), Term('B'), Term('N')

one, two, three = Constant('one'), Constant('two'), Constant('three')
four, five, six = Constant('four'), Constant('five'), Constant('six')
seven, eight, nine = Constant('seven'), Constant('eight'), Constant('nine')

# Dict to easily access variable names from index
square_dict = {
    "1" : one,
    "2" : two,
    "3" : three,
    "4" : four,
    "5" : five,
    "6" : six,
    "7" : seven,
    "8" : eight,
    "9" : nine
}

x = Constant('x')
o = Constant('o')
n = Constant('n')

turn = Term('turn')
query = Term('query')

C = Var('C')

p = SimpleProgram()

# Marks, cells, and initial state of board
p += mark(x)
p += mark(o)
p += mark(n)

p += board(n,n,n,n,n,n,n,n,n,0)

# Turns
for i in range(9):
    p += turn(Constant(i))

# Probability distributions for each cell
for i in range(9): 
    c = square_dict[str(i+1)]
    (good, bad, neutral) = probs[i]
    p += AnnotatedDisjunction([G(C, p=good), 
                               B(C, p=bad), 
                               N(C, p=neutral)],
                               C is c)
    
# Calculating next moves: Missing 

# Defining winning and losing: Missing
    
p += (win << board(n,n,n,n,n,n,n,n,n,0))
    
# Queries: Missing

p += query(win)
p += query(turn(5))
p += query(turn(10))

val = get_evaluatable().create_from(p).evaluate()

print(probs)
print(val)