import louiswork
import simulator
import game_logic

# 1/9::pos(1,1); 1/9::pos(2,1); 1/9::pos(3,1); 1/9::pos(4,1); 1/9::pos(5,1); 
#                1/9::pos(6,1); 1/9::pos(7,1); 1/9::pos(8,1); 1/9::pos(9,1).

def getUniformProbDist(state, turn_nr):
    cells = louiswork.available_cells(state)
    total = len(cells)
    probs = ""
    for i in range(total):
        probs += "1/{}::pos({},{})".format(total,str(i),turn_nr)
        if i < total - 1: 
            probs += "; "
    return probs + ".\n"



print(getUniformProbDist((None,"x",None,"o"),2))
    
