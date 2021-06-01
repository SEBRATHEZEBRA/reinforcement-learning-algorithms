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

    for i in range(k):

        x = getRandomX()
        y = getRandomY()

        while not checkFree(x, y):
            x = getRandomX()
            y = getRandomY()

        landmines.append([y, x])

def main():

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
            print(i)
            if argv[i] == "-start":
                print("in")
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


if __name__ == "__main__":
    main()
