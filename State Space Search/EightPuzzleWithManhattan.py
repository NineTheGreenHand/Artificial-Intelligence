'''EightPuzzleWithManhattan.py
by Sheng Yu
UWNetID: shengy23
Student number: 1736385

Assignment 2, Part 2, in CSE 415, Winter 2021.

This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
'''

from EightPuzzle import *

def h(s):
    '''We return an estimate of the Manhattan Distance
    between s and the goal state.'''

    goal = State([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    if goal_test(s):
        return 0
    else:
        dist = 0
        for i in range(0, 3):
            for j in range(0, 3):
                cur = s.b[i][j]
                g = goal.b[i][j]
                if cur == 0:            # We don't count the blank.
                    continue
                else:
                    x1 = cur % 3        # The x - location this tile should be.
                    y1 = cur // 3       # The y - location this tile should be.
                if g == 0:
                    x2 = 0              # The x - location this tile currently is.
                    y2 = 0              # The y - location this tile currently is.
                else:
                    x2 = g % 3          # The x - location this tile currently is.
                    y2 = g // 3         # The y - location this tile currently is.
                dist += abs(x1 - x2)    # Horizontal difference.
                dist += abs(y1 - y2)    # Vertical difference.
        return dist


# A simple test:
# print(h(State([[4, 0, 2], [1, 6, 3], [7, 8, 5]])))
# print(h(State([[3, 0, 1], [6, 4, 2], [7, 8, 5]])))