from problog.program import PrologString
from problog.core import ProbLog
from problog import get_evaluatable

# How to get this to work: 
# In vscode search bar: type ">" and search for "Python: Create Environment"
# Now create environment and inside it, run "python3 -m pip install problog" in vscode terminal 
# Now the environment and problog are installed in your tictactoe map 
# Running the file looks like this for me:     
# (.venv) Airvanlcaladmin:ProbTicTacToe djanira$ python3 djanira.py

p = PrologString("""
coin(c1). coin(c2).
0.4::heads(C); 0.6::tails(C) :- coin(C).
win :- heads(C).
evidence(heads(c1), false).
query(win).
""")

val = get_evaluatable().create_from(p).evaluate()
print(val)