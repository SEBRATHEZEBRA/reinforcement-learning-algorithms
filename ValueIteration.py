from sys import argv
from random import randint

iterations = []
states = []

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
minimum = 0.05

# Directions the robot can move.
directions = {
    "UP":[0, 1],
    "DOWN":[0, -1],
    "LEFT":[-1, 0],
    "RIGHT":[1, 0]
}

# Returns a random x value in the gridworld.
def getRandomX():
    return randint(0, width - 1)

# Returns a random y value in the gridworld.
def getRandomY():
    return randint(0, height - 1)

# Checks if the coordinates [x, y] are being used as the start state, end state or landmines.
def checkFree(x, y):

    if [x, y] in landmines or [x, y] == start or [x, y] == end:
        return False

    return True

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

def value(s, gamma, S, T, R, V):

    # Initialize values for all states to 0.
    for i in range(height):
        states.append([0] * width)

    # Initialize the end state to 100.
    states[end[0]][end[1]] = 100

    for s in states:



def main():

    if (len(argv) == 3):
        start[0] = getRandomX()
        start[1] = getRandomY()

        x = getRandomX()
        y = getRandomY()

        while not checkFree(x, y):
            x = getRandomX()
            y = getRandomY()

        end[0] = x
        end[1] = y

        for i in range(k):

            x = getRandomX()
            y = getRandomY()

            while not checkFree(x, y):
                x = getRandomX()
                y = getRandomY()

            landmines.append([x, y])


if __name__ == "__main__":
    main()
