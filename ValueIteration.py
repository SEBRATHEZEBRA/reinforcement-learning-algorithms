from sys import argv
from random import randint

states = []
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


def main():

    if (len(argv) < 3):
        print("Correct use: python3 Reinforcement.py <width> <height> [options]")
        return

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

    print(start, "", end)
    print(landmines)


if __name__ == "__main__":
    main()
