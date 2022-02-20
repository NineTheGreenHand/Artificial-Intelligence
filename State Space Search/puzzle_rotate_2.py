'''puzzle3.py
An instance of the Eight Puzzle.
'''

from EightPuzzleWithManhattan import *

# We simply redefine the initial state.

'''
init_state_list = [[6, 3, 0], 
                   [7, 4, 1], 
                   [8, 5, 2]]
'''
# init_state_list = [[3,0,1],[6,4,2],[7,8,5]]
# init_state_list = [[3,1,2],[6,8,7],[5,4,0]]
# init_state_list = [[4,5,0],[1,2,8],[3,7,6]]
init_state_list = [[0,8,2],[1,7,4],[3,6,5]]

CREATE_INITIAL_STATE = lambda: State(init_state_list)


