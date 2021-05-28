from sys import argv
from random import randint

states = []
width = 0
height = 0

# k is the number of landmines
landmines = []
k = 9

start = [0, 0]
end = [0, 0]

gamma = 0.9

directions = {
    "UP":[0, 1],
    "DOWN":[0, -1],
    "LEFT":[-1, 0],
    "RIGHT":[1, 0]
}


def main():

    if (len(argv) < 3):
        print("Correct use: python3 Reinforcement.py <width> <height> [options]")
        return

    width = int(argv[1])
    height = int(argv[2])

    if (len(argv) == 3):
        start[0] = randint(0, width - 1)
        start[1] = randint(0, height - 1)

        end[0] = randint(0, width - 1)
        end[1] = randint(0, height - 1)

        if start[0] == end[0]:
            end[0] = randint(0, width - 1)
        elif start[1] == end[1]:
            end[1] = randint(0, height - 1)

        for i in range(k):
            landmines.append([randint(0, width - 1), randint(0, height - 1)])
            if start[0] == landmines[i][0] or end[0] == landmines[i][0]:
                landmines[i][0] = randint(0, width - 1)
            elif start[1] == landmines[i][1] or end[1] == landmines[i][1]:
                landmines[i][1] = randint(0, height - 1)

    print(start, "", end)
    print(landmines)

    if [1, 2] in landmines:
        print("[1, 2] is a landmine.")



if __name__ == "__main__":
    main()
