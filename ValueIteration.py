import matplotlib.pyplot as plt

from sys import argv
from random import randint
from copy import deepcopy
from Animate import generateAnimat

records = []
states = []
previous = []
opt_pol = []

if (len(argv) < 3):
    print("Correct use: python3 Reinforcement.py <width> <height> [options]")
    exit()

width = int(argv[1])
height = int(argv[2])

# k is the number of landmines
landmines = []
k = 3

start = [0, 0]
end = [0, 0]

gamma = 0.9

# Directions the robot can move.
directions = {
    "UP":[-1, 0],
    "DOWN":[1, 0],
    "LEFT":[0, -1],
    "RIGHT":[0, 1]
}

# Returns a random x value in the gridworld.
def getRandomX():
    return randint(0, width - 1)

# Returns a random y value in the gridworld.
def getRandomY():
    return randint(0, height - 1)

# Checks if the coordinates (x, y) are being used as the start state, end state or landmines.
def checkFree(x, y):

    if [x, y] in landmines or [x, y] == start or [x, y] == end:
        return False

    return True

# Generates a random position for the start state.
def genRandomStart():
    start[0] = getRandomY()
    start[1] = getRandomX()

# Generates a random position for the end state.
def genRandomEnd():
    x = getRandomX()
    y = getRandomY()

    while not checkFree(x, y):
        x = getRandomX()
        y = getRandomY()

    end[0] = y
    end[1] = x

# Generates random positions for the landmines.
def genRandomMines():
    print(k)
    for i in range(k):

        x = getRandomX()
        y = getRandomY()

        while not checkFree(x, y):
            x = getRandomX()
            y = getRandomY()

        landmines.append([y, x])

# Returns a list of legal actions a robot can perform from a set of coordinates (x, y) in the grid.
def getLegalActions(x, y):

    legal = []
    if x == 0:
        legal.append("RIGHT")
    elif x == width - 1:
        legal.append("LEFT")
    else:
        legal.append("LEFT")
        legal.append("RIGHT")

    if y == 0:
        legal.append("DOWN")
    elif y == height - 1:
        legal.append("UP")
    else:
        legal.append("DOWN")
        legal.append("UP")

    return legal

# The value function
def value(x, y):

    legal = []
    legal = getLegalActions(x, y)

    # Add the values of each neighbouring state to the values array.
    values = []
    for move in legal:
        values.append(previous[y + directions[move][0]][x + directions[move][1]])

    # Getting the index of the max value.
    max = 0
    for i in range(1, len(values)):
        if values[i] > values[max]:
            max = i

    # My version of Bellman's equation but it doesn't include R.
    value = gamma * values[max]
    return round(value, 2)

# Finds the optimal policy.
def getOptPol():

    # Appending the starting state to the optimal policy.
    opt_pol.append((start[0], start[1]))
    y = start[0]
    x = start[1]

    while True:

        legal = []
        legal = getLegalActions(x, y)

        # Add the values of each neighbouring state to the values array.
        values = []
        for move in legal:
            values.append(states[y + directions[move][0]][x + directions[move][1]])

        # Getting the index of the max value.
        max = 0
        for i in range(1, len(values)):
            if values[i] > values[max]:
                max = i

        # Getting the coordinates of the max value.
        y += directions[legal[max]][0]
        x += directions[legal[max]][1]

        opt_pol.append((y, x))

        # Checking if we have reached the end state yet.
        if [y, x] == end:
            break

# Starts the value iteration algorithm
def startVI():

    # Initialize values for all states to 0.
    for i in range(height):
        states.append([0] * width)
        previous.append([0] * width)

    # Initialize the end state to 100.
    states[end[0]][end[1]] = 100
    states[start[0]][start[1]] = 0

    # Initializing the landmines to -100.
    for i in landmines:
        states[i[0]][i[1]] = -100

    i = 0
    while True:

        records.append(deepcopy(states))

        # Making a deepcopy of the states to previous
        for i in range(height):
            for j in range(width):
                previous[i][j] = states[i][j]

        # For each state I update the value of the next iteration.
        for y in range(height):
            for x in range(width):
                if [y, x] != start and [y, x] != end and [y, x] not in landmines:
                    states[y][x] = value(x, y)

        # Convergence condition is that there is on change between the previous and current states.
        if previous == states and i > 0:
            break

        i += 1


def main():

    global k
    # Checking if any options are selected.
    if len(argv) == 3:
        genRandomStart()
        genRandomEnd()
        genRandomMines()

    # Triggering the correct actions when ceratin options are selected.
    elif len(argv) > 3:

        if "-start" not in argv:
            genRandomStart()

        if "-end" not in argv:
            genRandomEnd()

        i = 3
        while i < len(argv):
            if argv[i] == "-start":
                start[0] = int(argv[i + 2])
                start[1] = int(argv[i + 1])
                i += 3
            elif argv[i] == "-end":
                end[0] = int(argv[i + 2])
                end[1] = int(argv[i + 1])
                i += 3
            elif argv[i] == "-k":
                k = int(argv[i + 1])
                genRandomMines()
                i += 2
            elif argv[i] == "-gamma":
                gamma = float(argv[i + 1])
                i += 2
            else:
                print("Incorrect option.")
                print("Correct options are:")
                print("-start xpos ypos")
                print("-end xpos ypos")
                print("-k num")
                print("-gamma g")
                return

    startVI()
    getOptPol()

    generateAnimat(records, start, end, mines=landmines, opt_pol=opt_pol, start_val=0, end_val=100, mine_val=-1, just_vals=False, generate_gif=False, vmin = -1, vmax = 100)
    plt.show()


if __name__ == "__main__":
    main()
