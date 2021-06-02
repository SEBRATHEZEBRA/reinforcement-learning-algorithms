# Reinforcement Learning
## Q-Learning program isn't working all the time.
## File used
Animate.py: Code given in order to animate the results, I modified it by switching the x and y coordinates around as that is how I implemented my program.

ValueIteration.py: Contains my implementation of the Value Iteration algorithm using Bellman's equation in a deterministic environment.

QLearning.py: Contains my implementation of the Q-Learning algorithm using Bellman's equation in a deterministic environment.

Makefile: Runs the different algorithms, as well as sets up a virtual environment and removes the virtual environment if needed.

requirements.txt: Contains the packages used when setting up the virtual environment.

## Usage
To set up the virtual environment:
```bash
make
```

To remove the virtual environment:
```bash
make clean
```

To run ValueIteration.py program with a set width and height:
```bash
make virun
```

To run QLearning.py program with a set width and height:
```bash
make qlrun
```
