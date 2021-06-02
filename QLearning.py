import matplotlib.pyplot as plt

from sys import argv
from random import randint
from copy import deepcopy
from time import perf_counter
from Animate import generateAnimat

records = []
opt_pol = []

# Q-table format is: 0 - coordinates in gridworld, 1 - left, 2 - right, 3 - up, 4 - down
qTable = []

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

# Learning rate
n = 0.8

# Number of episodes
e = 10000

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

    if [y, x] in landmines or [y, x] == start or [y, x] == end:
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

# Returns the index in the Q-table for a set of coordinates.
def getQIndex(x, y):

    for i in range(height * width):
        if qTable[i][0] == [y, x]:
            return i

    i = -1
    return i

# Returns the index of the direction specified.
def getDI(direction):

    if direction == "LEFT":
        return 1
    elif direction == "RIGHT":
        return 2
    elif direction == "UP":
        return 3
    elif direction == "DOWN":
        return 4
    else:
        return -1

# Returns the max value of known actions.
def maxValue(x, y):

    legal = []
    legal = getLegalActions(x, y)
    qIndex = getQIndex(x, y)

    # Add the values of each neighbouring state to the values array.
    values = []
    for move in legal:
        i = getDI(move)
        values.append(qTable[qIndex][i])

    # Getting the index of the max value.
    max = 0
    for i in range(1, len(values)):
        if values[i] > values[max]:
            max = i

    return values[max]

# Adds the record of the current episode to the records array.
def addRecord():

    r = []
    for i in range(height):
        r.append([0] * width)

    for i in range(height * width):

        y = qTable[i][0][0]
        x = qTable[i][0][1]

        y1 = qTable[i][0][0]
        x1 = qTable[i][0][1]

        legal = []
        legal = getLegalActions(x, y)

        for move in legal:

            d = getDI(move)
            x1 = x + directions[move][1]
            y1 = y + directions[move][0]

            value = qTable[i][d]
            if value > r[y1][x1]:
                r[y1][x1] = value

    records.append(r)

# Finds the optimal policy.
def getOptPol():

    # Appending the starting state to the optimal policy.
    opt_pol.append((start[0], start[1]))
    y = start[0]
    x = start[1]
    previous = []
    time = perf_counter()

    s = 0
    while True:

        legal = []
        legal = getLegalActions(x, y)

        # Add the values of each neighbouring state to the values array.
        values = []
        for move in legal:
            values.append(records[e - 1][y + directions[move][0]][x + directions[move][1]])

        # Getting the index of the max value.
        max = 0
        maxValue = values[max]

        coords = [y + directions[legal[max]][0], x + directions[legal[max]][1]]
        if coords in previous:
            maxValue = -1

        for i in range(1, len(values)):

            coords = [y + directions[legal[max]][0], x + directions[legal[max]][1]]

            if values[i] > maxValue and coords not in previous:
                max = i
                maxValue = values[i]

        # Getting the coordinates of the max value.
        y += directions[legal[max]][0]
        x += directions[legal[max]][1]

        # Adding the coordinates to the optimal policy array.
        previous.append([y, x])
        opt_pol.append((y, x))

        # Timing out if optimal policy isn't being found.
        diff = perf_counter() - time
        if diff > 5:
            print("Optimal policy not found, stuck in a loop between coords again.")
            break

        # Checking if we have reached the end state yet.
        if [y, x] == end:
            break

# Starts the Q-Learning.
def startQL():

    # Initializing the qTable to 0.
    x = 0
    y = 0
    for i in range(height * width):

        qTable.append([0] * 5)
        if i % width == 0 and i > 0:
            x = 0
            y += 1

        qTable[i][0] = [y, x]
        x += 1

    # Running for a total of e episodes.
    for i in range(e):

        # Selecting a random inital current state
        current = [randint(0, height - 1), randint(0, width - 1)]
        currentI = getQIndex(current[1], current[0])

        while current != end and current not in landmines:

            # Getting a random action for the current state.
            legal = []
            legal = getLegalActions(current[1], current[0])
            x = randint(0, len(legal) - 1)
            d = legal[x]
            randAct = directions[d]
            dir = getDI(d)

            # Getting the coordinates of the next state.
            next = [current[0] + randAct[0], current[1] + randAct[1]]
            nextI = getQIndex(next[1], next[0])

            if next in landmines:
                reward = -100
            elif next == end:
                reward = 100
            else:
                reward = 0

            # Calculating the q-value of the current state.
            qTable[currentI][dir] = qTable[currentI][dir] + n * (reward + gamma * maxValue(next[1], next[0]) - qTable[currentI][dir])
            qTable[currentI][dir] = round(qTable[currentI][dir], 2)

            # Setting the next state as the current state.
            current[0] = next[0]
            current[1] = next[1]

        addRecord()

def main():

    global k
    global n
    global e

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

        if "-k" not in argv:
            genRandomMines()

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
                i += 2
                genRandomMines()

            elif argv[i] == "-gamma":
                gamma = float(argv[i + 1])
                i += 2

            elif argv[i] == "-learning":
                n = float(argv[i + 1])
                i += 2

            elif argv[i] == "-epochs":
                e = int(argv[i + 1])
                i += 2

            else:
                print("Incorrect option.")
                print("Correct options are:")
                print("-start xpos ypos")
                print("-end xpos ypos")
                print("-k num")
                print("-gamma g")
                print("-learning n")
                print("-epochs e")
                return

    startQL()
    getOptPol()
    generateAnimat(records, start, end, mines=landmines, opt_pol=opt_pol, start_val=0, end_val=100, mine_val=-100, just_vals=False, fps = 250, vmin = -100, vmax = 100)
    plt.show()


if __name__ == "__main__":
    main()
