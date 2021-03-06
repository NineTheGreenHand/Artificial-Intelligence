"""Q_Learn.py
STUDENT STARTER TEMPLATE ...

Implement Q-Learning in this file by completing the implementations
of the functions whose stubs are present.
Add or change code wherever you see #*** ADD OR CHANGE CODE HERE ***

This is part of the UW Intro to AI Starter Code for Reinforcement Learning.

"""

import random


# Edit the returned name to ensure you get credit for the assignment.
def student_name():
    return "Yu, Sheng"


STATES = None
ACTIONS = None
UQV_callback = None
Q_VALUES = {}
is_valid_goal_state = None
Terminal_state = None
USE_EXPLORATION_FUNCTION = None
INITIAL_STATE = None


def setup(states, actions, q_vals_dict, update_q_value_callback,
          goal_test, terminal, use_exp_fn=False):
    """This method is called by the GUI the first time a Q_Learning
    menu item is selected. It may be called again after the user has
    restarted from the File menu.
    Q_VALUES starts out with all Q-values at 0.0 and a separate key
    for each (s, a) pair."""
    global STATES, ACTIONS, UQV_callback, Q_VALUES, is_valid_goal_state
    global USE_EXPLORATION_FUNCTION, Terminal_state
    STATES = states
    ACTIONS = actions
    Q_VALUES = q_vals_dict
    UQV_callback = update_q_value_callback
    is_valid_goal_state = goal_test
    Terminal_state = terminal
    USE_EXPLORATION_FUNCTION = use_exp_fn
    if USE_EXPLORATION_FUNCTION:
        # *** ADD OR CHANGE CODE HERE ***
        # Change this if you implement an exploration function:
        print("You have not implemented an exploration function")


PREVIOUS_STATE = None
LAST_ACTION = None


def set_starting_state(s):
    """This is called by the GUI when a new episode starts.
    Do not change this function."""
    global INITIAL_STATE, PREVIOUS_STATE
    print("In Q_Learn, setting the starting state to " + str(s))
    INITIAL_STATE = s
    PREVIOUS_STATE = s


ALPHA = 0.5
CUSTOM_ALPHA = False
EPSILON = 0.5
CUSTOM_EPSILON = False
GAMMA = 0.9


def set_learning_parameters(alpha, epsilon, gamma):
    """ Called by the system. Do not change this function."""
    global ALPHA, EPSILON, CUSTOM_ALPHA, CUSTOM_EPSILON, GAMMA
    ALPHA = alpha
    EPSILON = epsilon
    GAMMA = gamma
    if alpha < 0:
        CUSTOM_ALPHA = True
    else:
        CUSTOM_ALPHA = False
    if epsilon < 0:
        CUSTOM_EPSILON = True
    else:
        CUSTOM_EPSILON = False


def update_Q_value(previous_state, previous_action, new_value):
    """Whenever your code changes a value in Q_VALUES, it should
    also call this method, so the changes can be reflected in the
    display.
    Do not change this function."""
    UQV_callback(previous_state, previous_action, new_value)


def handle_transition(action, new_state, r):
    """When the user drives the agent, the system will call this function,
    so that you can handle the learning that should take place on this
    transition."""
    global PREVIOUS_STATE, Q_VALUES, GAMMA
    current_qv = Q_VALUES[(PREVIOUS_STATE, action)]
    max_qp = 0  # max_a' Q(s', a')
    for pair in Q_VALUES:
        if pair[0] == new_state:
            max_qp = max(max_qp, Q_VALUES[pair])
    new_qv = (1 - ALPHA) * current_qv + ALPHA * (r + GAMMA * max_qp)
    # Update the existing Q-value for (s, a)
    Q_VALUES[(PREVIOUS_STATE, action)] = new_qv
    # You should call update_Q_value before returning.
    update_Q_value(PREVIOUS_STATE, action, new_qv)
    print("Transition to state: " + str(new_state) + \
          "\n with reward " + str(r) + " is currently not handled by your program.")
    PREVIOUS_STATE = new_state


def choose_next_action(s, r, terminated=False):
    """When the GUI or engine calls this, the agent is now in state s,
     and it receives reward r.
     If terminated==True, it's the end of the episode, and this method
      can just return None after you have handled the transition.

     Use this information to update the q-value for the previous state
     and action pair.

     Then the agent needs to choose its action and return that.

     """
    global INITIAL_STATE, PREVIOUS_STATE, LAST_ACTION, ALPHA, EPSILON, Terminal_state, \
        CUSTOM_EPSILON, CUSTOM_ALPHA, GAMMA, ACTIONS
    # Unless s is the initial state, compute a new q-value for the
    # previous state and action.
    if not (s == INITIAL_STATE):
        max_qp = 0
        for pair in Q_VALUES:
            if pair[0] == s:
                max_qp = max(max_qp, Q_VALUES[pair])
        previous_qv = Q_VALUES[(PREVIOUS_STATE, LAST_ACTION)]

        # Compute your update here.
        # if CUSTOM_ALPHA is True, manage the alpha values over time.
        if CUSTOM_ALPHA:
            if ALPHA < 0:
                ALPHA = 0.1
            elif ALPHA >= 1:
                ALPHA = 1
            else:
                ALPHA += 0.00001
        # print("Now, my ALPHA is: " + str(ALPHA))  # For debugging
        # Otherwise go with the fixed value.
        new_qval = (1 - ALPHA) * previous_qv + ALPHA * (r + GAMMA * max_qp)

        # Save it in the dictionary of Q_VALUES:
        Q_VALUES[(PREVIOUS_STATE, LAST_ACTION)] = new_qval

        # Then let the Engine and GUI know about the new Q-value.
        update_Q_value(PREVIOUS_STATE, LAST_ACTION, new_qval)

    # Now select an action according to your Q-Learning criteria, such
    # as expected discounted future reward vs exploration.

    if USE_EXPLORATION_FUNCTION:
        # Change this if you implement an exploration function:
        # *** ADD OR CHANGE CODE HERE ***
        print("You have not implemented an exploration function")

    if terminated:
        some_action = None
    elif is_valid_goal_state(s):
        print("It's a goal state; return the Exit action.")
        some_action = "Exit"
    elif s == Terminal_state:
        # print("It's not a goal state. But if it's the special Terminal state, return None.")
        some_action = None
    else:
        # If EPSILON > 0, or CUSTOM_EPSILON is True,
        # then use epsilon-greedy learning here.
        # In order to access q-values, simply get them from the dictionary, e.g.,
        # some_qval = Q_VALUES[(some_state, some_action)]
        # print("it's neither a goal nor the Terminal state, so return some ordinary action.")
        all_s_actions = []
        for pair in Q_VALUES:
            if pair[0] == s and pair[1] != "Exit":
                all_s_actions.append(pair[1])
        actions_list_length = len(all_s_actions)
        # print(str(all_s_actions))   # For debugging
        if CUSTOM_EPSILON:
            if EPSILON >= 0.0002:
                EPSILON -= 0.00001
            elif EPSILON < 0:
                EPSILON = 0.99
            else:
                EPSILON = 0
        p = random.random()
        # print("Now, the EPSILON value is " + str(EPSILON)) # For debugging
        if p < EPSILON:
            some_action = all_s_actions[random.randrange(0, actions_list_length)]
            # print("My action is: (random)" + some_action) # For debugging
        else:
            max_qv = 0
            max_a = ACTIONS[0]
            for a in ACTIONS:
                val = Q_VALUES[(s, a)]
                if val > max_qv and a != "Exit":
                    max_a = a
            some_action = max_a
            # print("My action is: (optimal)" + some_action) # For debugging
    LAST_ACTION = some_action  # remember this for next time
    PREVIOUS_STATE = s
    return some_action


Policy = {}


def extract_policy(S, A):
    """Return a dictionary mapping states to actions. Obtain the policy
   using the q-values most recently computed.
   Ties between actions having the same (s, a) value can be broken arbitrarily.
   Reminder: goal states should map to the Exit action, and no other states
   should map to the Exit action.
   """
    global Policy
    Policy = {}
    for state in S:
        max_qv = 0
        action = ACTIONS[0]
        if is_valid_goal_state(state):
            action = "Exit"
        else:
            for a in A:
                if Q_VALUES[(state, a)] > max_qv and a != "Exit":
                    max_qv = Q_VALUES[(state, a)]
                    action = a
        Policy[state] = action
    return Policy
