import louiswork as louiswork
import trash.simulator as simulator
import trash.nano as nano

def win_strategy(grid, state):
    probabilities = 0
    cells = louiswork.available_cells(state)
    for cell in cells:
        probwin = query(louiswork.apply(state, cell, "x"), grid, win)
        probabilities.append(cell, probwin) 
    return cells(probabilities.index(max(probabilities)))

