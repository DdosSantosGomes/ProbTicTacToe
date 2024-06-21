import strategies.louiswork as louiswork
import simulator
import nano

def lose_strategy(grid, state):
    probabilities = 0
    cells = louiswork.available_cells(state)
    for cell in cells:
        probwin = query(louiswork.apply(state, cell, "x"), grid, lose)
        probabilities.append(cell, probwin) 
    return cells(probabilities.index(min(probabilities)))

