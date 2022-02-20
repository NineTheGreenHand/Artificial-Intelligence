"""ValueIteration.py
STUDENT STARTER TEMPLATE FOR ...
Value Iteration for Markov Decision Processes.
"""


# Edit the returned name to ensure you get credit for the assignment.
def student_name():
    return "Yu, Sheng"


Vkplus1 = {}
Q_Values_Dict = {}
one_step_of_VI_called = False


def one_step_of_VI(S, A, T, R, gamma, Vk):
    """S is list of all the states defined for this MDP.
     A is a list of all the possible actions.
     T is a function representing the MDP's transition model.
     R is a function representing the MDP's reward function.
     gamma is the discount factor.
     The current value of each state s is accessible as Vk[s].
    """

    """Your code should fill the dictionaries Vkplus1 and Q_Values_dict
      with a new value for each state, and each q-state, and assign them
      to the state's and q-state's entries in the dictionaries, as in
          Vkplus1[s] = new_value
          Q_Values_Dict[(s, a)] = new_q_value

      Also determine delta_max, which we define to be the maximum
      amount that the absolute value of any state's value is changed
      during this iteration.
    """
    global one_step_of_VI_called
    one_step_of_VI_called = True
    global Q_Values_Dict
    delta_max = 0
    for state in S:
        max_action_value = 0
        for action in A:
            q = 0
            for s_ in S:
                q += T(state, action, s_) * (R(state, action, s_) + gamma * Vk[s_])
            Q_Values_Dict[(state, action)] = q
            max_action_value = max(max_action_value, q)  # V* we have for state after iteration
        current_value = Vk[state]  # V* we have for state before iteration
        difference = abs(current_value - max_action_value)
        delta_max = max(delta_max, difference)
        Vkplus1[state] = max_action_value
    return Vkplus1, delta_max


def return_Q_values(S, A):
    """Return the dictionary whose keys are (state, action) tuples,
     and whose values are floats representing the Q values from the
     most recent call to one_step_of_VI. This is the normal case, and
     the values of S and A passed in here can be ignored.
     However, if no such call has been made yet, use S and A to
     create the answer dictionary, and use 0.0 for all the values.
    """
    if one_step_of_VI_called:
        return Q_Values_Dict
    else:
        for state in S:
            for action in A:
                Q_Values_Dict[(state, action)] = 0.0
        return Q_Values_Dict


Policy = {}


def extract_policy(S, A):
    """Return a dictionary mapping states to actions. Obtain the policy
    using the q-values most recently computed.  If none have yet been
    computed, call return_Q_values to initialize q-values, and then
    extract a policy.  Ties between actions having the same (s, a) value
    can be broken arbitrarily.
    """
    global Policy
    Policy = {}
    Q_Values_Dict = return_Q_values(S, A)
    for s_a_pair in Q_Values_Dict:
        state = s_a_pair[0]
        action = s_a_pair[1]
        evaluation = Q_Values_Dict[s_a_pair]
        for pair in Q_Values_Dict:
            curr_s = pair[0]
            if curr_s == state and evaluation < Q_Values_Dict[pair]:
                evaluation = Q_Values_Dict[pair]
                action = pair[1]
        Policy[state] = action
    return Policy


def apply_policy(s):
    """Return the action that your current best policy implies for state s."""
    global Policy
    return Policy[s]