import louiswork as louiswork
import trash.simulator as simulator
import trash.nano as nano

def lose_strategy(grid, state):
    probabilities = 0
    cells = louiswork.available_cells(state)
    for cell in cells:
        probwin = query(louiswork.apply(state, cell, "x"), grid, lose(2))
        probabilities.append(cell, probwin) 
    return cells(probabilities.index(min(probabilities)))

