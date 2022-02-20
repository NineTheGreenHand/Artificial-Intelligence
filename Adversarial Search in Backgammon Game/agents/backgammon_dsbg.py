'''
Group Members:

Name: Qiaoxue Liu
UW netid: qiaoxl

Name: Sheng Yu
UW netid: shengy23

This file is an modification on the starter code given
in a3-starter, CSE 415. "Deterministic Simplified Backgammon"
is implemented in this file.
'''

from game_engine import genmoves

W = 0
R = 1

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.state_counter = 0
        self.cutoff_counter = 0
        self.maxply = 2
        self.prune = False

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        return "qiaoxl & shengy23"

    # If prune==True, changes the search algorithm from minimax
    # to Alpha-Beta Pruning
    def useAlphaBetaPruning(self, prune=False):
        self.state_counter = 0
        self.cutoff_counter = 0
        self.prune = prune

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        return self.state_counter, self.cutoff_counter

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. If maxply==-1,
    # no limit is set
    def setMaxPly(self, maxply=-1):
        self.maxply = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        if func is not None:
            self.staticEval = func

    def initialize_move_gen_for_state(self, state, who, die1=1, die2=6):
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
    def move(self, state, die1=1, die2=6):
        self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        moves = self.get_all_moves()
        temp = {}
        l = list(moves.keys())[:]
        for m in l:
            if moves[m] is not None:
                if self.prune:
                    eval = self.alpha_beta(self.maxply, moves[m], -100000000, 100000000, die1, die2)
                else:
                    eval = self.minimax(self.maxply, moves[m], die1, die2)
                temp[eval] = m
        if state.whose_move == W and bool(temp):
            maxEval = max(list(temp.keys())[:])
            return temp[maxEval]
        elif state.whose_move == R and bool(temp):
            minEval = min(list(temp.keys())[:])
            return temp[minEval]
        return 'p'

    # Find all the possible moves
    def get_all_moves(self):
        """Uses the mover to generate all legal moves."""
        move_list = {}
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_list[m[0]] = m[1]
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list['p'] = None
        return move_list

    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R
    def staticEval(self, state):
        curr_state = state.pointLists
        value = 0
        for i in range(0, 24):
            temp = curr_state[i]
            if W in temp:
                value += (i + 1) * temp.count(W) * 10
            elif R in temp:
                value += (i - 24) * temp.count(R) * 5
        barElement = state.bar
        whiteBearOff = state.white_off
        redBearOff = state.red_off
        if len(barElement) != 0:
            value -= barElement.count(W) * 100
            value += barElement.count(R) * 100
        if len(whiteBearOff) != 0:
            value += len(whiteBearOff) * 1000
        if len(redBearOff) != 0:
            value -= len(redBearOff) * 500
        return value

    # The method to define minimax
    def minimax(self, depth, state, die1, die2):
        if depth == 0 or len(state.red_off) == 15 or len(state.white_off) == 15:
            return self.staticEval(state)
        self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        s = self.get_all_moves()
        if state.whose_move == W:
            maxEval = -100000000
            for child in s.values():
                if child is not None:
                    self.state_counter += 1
                    eval = self.minimax(depth - 1, child, die1, die2)
                    maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = 100000000
            for child in s.values():
                if child is not None:
                    self.state_counter += 1
                    eval = self.minimax(depth - 1, child, die1, die2)
                    minEval = min(minEval, eval)
            return minEval

    # The method to define alpha beta pruning
    def alpha_beta(self, depth, state, alpha, beta, die1, die2):
        if depth == 0 or len(state.red_off) == 15 or len(state.white_off) == 15:
            return self.staticEval(state)
        self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        s = self.get_all_moves()
        if state.whose_move == W:
            maxEval = -100000000
            for child in s.values():
                if child is not None:
                    self.state_counter += 1
                    eval = self.alpha_beta(depth - 1, child, alpha, beta, die1, die2)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if alpha >= beta:
                        self.cutoff_counter += 1
                        break
            return maxEval
        else:
            minEval = 100000000
            for child in s.values():
                if child is not None:
                    self.state_counter += 1
                    eval = self.alpha_beta(depth - 1, child, alpha, beta, die1, die2)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if alpha >= beta:
                        self.cutoff_counter += 1
                        break
            return minEval








