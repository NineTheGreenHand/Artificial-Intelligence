"""binary_perceptron.py
One of the starter files for use in CSE 415, Winter 2021
Assignment 6.

Version of Feb. 18, 2021

Student name: Sheng Yu
UW NetID: shengy23

"""


def student_name():
    return "Sheng Yu"


def classify(weights, x_vector):
    """Assume weights = [w_0, w_1, ..., w_{n-1}, biasweight]
    Assume x_vector = [x_0, x_1, ..., x_{n-1}]
    Note that y (correct class) is not part of the x_vector.
    Return +1 if the current weights classify this as a Positive,
    or  -1 if it seems to be a Negative.
    """
    # s is the sum of dot product of weights and x_vector
    s = 0
    for i in range(0, len(x_vector)):
        s += weights[i] * x_vector[i]
    s += weights[-1]
    if s >= 0:
        return 1
    else:
        return -1


def train_with_one_example(weights, x_vector, y, alpha):
    """Assume weights are as in the above function classify.
    Also, x_vector is as above.
    Here y should be +1 if x_vector represents a positive example,
    and -1 if it represents a negative example.
    Learning rate is specified by alpha.
    """
    check = classify(weights, x_vector)
    if y == 1:
        if check == -1:
            for i in range(0, len(x_vector)):
                weights[i] = weights[i] + alpha * x_vector[i]
            weights[-1] += alpha   # xn here is 1
            return weights, True
    else:
        if check == 1:
            for i in range(0, len(x_vector)):
                weights[i] = weights[i] - alpha * x_vector[i]
            weights[-1] -= alpha   # xn here is 1
            return weights, True
    return weights, False


# From here on use globals that can be easily imported into other modules.
WEIGHTS = [0, 0, 0]
ALPHA = 0.5


def train_for_an_epoch(training_data, reporting=True):
    """Go through the given training examples once, in the order supplied,
    passing each one to train_with_one_example.
    Update the global WEIGHT vector and return the number of weight updates.
    (If zero, then training has converged.)
    """
    global WEIGHTS, ALPHA
    changed_count = 0
    for data in training_data:
        y = data[-1]
        x_vector = data[:-1]
        pair = train_with_one_example(WEIGHTS, x_vector, y, ALPHA)
        if pair[1] is True:
            changed_count += 1
            WEIGHTS = pair[0]
    return changed_count


TEST_DATA = [
    [-2, 7, +1],
    [1, 10, +1],
    [3, 2, -1],
    [5, -2, -1]]


def test():
    print("Starting test with 3 epochs.")
    for i in range(3):
        train_for_an_epoch(TEST_DATA)
    print(WEIGHTS)
    print("End of test.")


if __name__ == '__main__':
    test()
