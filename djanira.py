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


# Louis Abraham's random probability distribution and grid generator
def generate_cell():
    neutral = random.choice(range(5, 35, 5))
    success = random.choice(range(30, 100 - neutral + 5, 5))
    failure = 100 - neutral - success
    return success / 100, neutral / 100, failure / 100

def generate_grid():
    return tuple(generate_cell() for _ in range(9))

probs = generate_grid() 

# we want: 
# p1::square1G; p2::square1B; p3::square1N  
# p1::square2G; p2::square2B; p3::square2N  
# p1::square3G; p2::square3B; p3::square3N  
# p1::square4G; p2::square4B; p3::square4N  
# p1::square5G; p2::square5B; p3::square5N  
# p1::square6G; p2::square6B; p3::square6N  
# p1::square7G; p2::square7B; p3::square7N  
# p1::square8G; p2::square8B; p3::square8N  
# p1::square9G; p2::square9B; p3::square9N

mark, x, o, n, board = Term('mark'), Term('x'), Term('o'), Term('n'), Term('board')
query = Term('query')

square1G, square2G, square3G = Var('square1G'), Var('square2G'), Var('square3G')
square4G, square5G, square6G = Var('square1G'), Var('square2G'), Var('square3G')
square7G, square8G, square9G = Var('square1G'), Var('square2G'), Var('square3G')

square1B, square2B, square3B = Var('square1B'), Var('square2B'), Var('square3B')
square4B, square5B, square6B = Var('square1B'), Var('square2B'), Var('square3B')
square7B, square8B, square9B = Var('square1B'), Var('square2B'), Var('square3B')

square1N, square2N, square3N = Var('square1N'), Var('square2N'), Var('square3N')
square4N, square5N, square6N = Var('square1N'), Var('square2N'), Var('square3N')
square7N, square8N, square9N = Var('square1N'), Var('square2N'), Var('square3N')

# Dict to easily access variable names from index
square_dict = {
    "1" : (square1G, square1B, square1N)
}

p = SimpleProgram()

p += mark(Constant('x'))
p += mark(Constant('o'))
p += mark(Constant('n'))
p += board(n,n,n,n,n,n,n,n,n)

for i in range(1,10):
    (g, b, n) = probs[i] 
    # p += AnnotatedDisjunction([square(C,p=0.4), tails(C,p=0.6)], coin(C))

# p += AnnotatedDisjunction([heads(C,p=0.4), tails(C,p=0.6)], coin(C))
# p += (win << heads(C))
# p += query(win)



val = get_evaluatable().create_from(p).evaluate()

print(probs)
print(val)