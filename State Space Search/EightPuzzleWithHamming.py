'''EightPuzzleWithHamming.py
by Sheng Yu
UWNetID: shengy23
Student number: 1736385

Assignment 2, Part 2, in CSE 415, Winter 2021.

This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
'''

from EightPuzzle import *

def h(s):
    '''We return an estimate of the Hamming Distance
    between s and the goal state.'''

    goal = State([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    if goal_test(s):
        return 0
    else:
        dist = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if s.b[i][j] != 0 and s.b[i][j] != goal.b[i][j]:
                    dist += 1
        return dist


# A simple test:
# print(h(State([[1, 0, 2], [3, 4, 6], [5, 7, 8]])))
