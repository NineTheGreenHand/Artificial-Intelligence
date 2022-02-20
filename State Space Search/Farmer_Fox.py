'''Farmer_Fox.py
by Sheng Yu
UWNetID: shengy23
Student number: 1736385

Assignment 2, Part 1, in CSE 415, Winter 2021.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

#<COMMON_CODE>
F = [0, 'F']     # mark farmer with char 'F', index 0
f = [1, 'f']     # mark fox with char 'f', index 1
c = [2, 'c']     # mark chicken with char 'c', index 2
g = [3, 'g']     # mark grain with char 'g', index 3

class State:
    def __init__(self, d):
        self.d = d

    def __eq__(self, s2):
        for side in ['left', 'right']:
            if self.d[side] != s2.d[side]:
                return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        txt = "["
        for side in ['left', 'right']:
            txt += str(self.d[side]) + " ,"
        return txt[:-2]+"]"

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        for side in ['left', 'right']:
            news.d[side] = self.d[side][:]
        return news

    def can_move(self, From, To, passenger):
        '''Tests whether it's legal to move one of the object
            along with the farmer across the river.'''
        pf = self.d[From]                           # Objects on the From side.
        if F[1] not in pf:                          # If Farmer not in From side, cannot move.
            return False
        if passenger == [F]:                        # if farmer move alone.
            if f[1] in pf and c[1] in pf:
                return False                        # leave chicken and fox together.
            elif c[1] in pf and g[1] in pf:
                return False                        # leave chicken and grain together.
            else:
                return True
        if passenger[1][1] not in pf:
            return False                            # Can't take object if not there.
        remain_pf = pf[:]
        remain_pf.remove(F[1])
        remain_pf.remove(passenger[1][1])           # Remaining objects on the From side.
        if f[1] in remain_pf and c[1] in remain_pf:
            return False                            # leave chicken and fox together.
        if c[1] in remain_pf and g[1] in remain_pf:
            return False                            # leave chicken and grain together.
        return True

    def move(self, From, To, passenger):
        '''Assuming it's legal to make the move, this computes
           the new state resulting from moving one object to
           the other side of the river.'''
        news = self.copy()                              # start with a deep copy.
        pf = self.d[From]                               # objects on the From side.
        pt = self.d[To]                                 # Objects on the To side.
        pf_temp = pf[:]
        pt_temp = pt[:]
        for p in passenger:
            pf_temp.remove(p[1])
            pt_temp.insert(p[0], p[1])
        if g[1] in pt_temp and pt_temp[-1] != g[1]:     # Make sure the order is always F, f, c, g
            pt_temp.remove(g[1])
            pt_temp.insert(g[0], g[1])
        news.d[From] = pf_temp                          # Update.
        news.d[To] = pt_temp                            # Update.
        return news                                     # Return new state.


def goal_test(s):
    '''If all objects (F, f, c, g) on the Right side, then s is a goal state.'''
    return s.d['left'] == []


def goal_message(s):
    return "Congratulations on successfully moving Farmer, Fox, Chicken and Grain across the river!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)
#</COMMON_CODE>


#<INITIAL_STATE>
INITIAL_DICT = {'left': ['F', 'f', 'c', 'g'], 'right': []}
CREATE_INITIAL_STATE = lambda: State(INITIAL_DICT)
#</INITIAL_STATE>

#<OPERATORS>
lrp_combinations = [('left', 'right', [F]), ('right', 'left', [F]),
                    ('left', 'right', [F, f]), ('right', 'left', [F, f]),
                    ('left', 'right', [F, c]), ('right', 'left', [F, c]),
                    ('left', 'right', [F, g]), ('right', 'left', [F, g])]
OPERATORS = [Operator(
  "Cross from " + fr + " to " + to + " with passenger: " + str(p) + ".",
  lambda s, fr1=fr, to1=to, p1=p: s.can_move(fr1, to1, p1),
  lambda s, fr1=fr, to1=to, p1=p: s.move(fr1, to1, p1))
  for (fr, to, p) in lrp_combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>