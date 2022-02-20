"""ternary_perceptron.py
Complete this python file as part of Part B.
You'll be filling in with code to implement:

a 3-way classifier
a 3-way weight updater

This program can be run from the given Python program
called run_3_class_4_feature_iris_data.py.


"""


def student_name():
    return "Sheng Yu"


def classify(W, x_vector):
    """Assume W = [W0, W1, W2] where each Wi is a vector of
    weights = [w_0, w_1, ..., w_{n-1}, biasweight]
    Assume x_vector = [x_0, x_1, ..., x_{n-1}]
    Note that y (correct class) is not part of the x_vector.
    Return 0, 1, or 2,
    depending on which weight vector gives the highest
    dot product with the x_vector augmented with the 1 for bias
    in position n.
    """
    eval_list = []
    for i in range(0, len(W)):
        s = 0
        for j in range(0, len(x_vector)):
            s += W[i][j] * x_vector[j]
        s += W[i][-1]
        eval_list.append(s)
    return argmax(eval_list)


# Helper function for finding the arg max of elements in a list.
# It returns the index of the first occurrence of the maximum value.
def argmax(lst):
    idx, mval = -1, -1E20
    for i in range(len(lst)):
        if lst[i] > mval:
            mval = lst[i]
            idx = i
    return idx


def train_with_one_example(W, x_vector, y, alpha):
    """Assume weights are as in the above function classify.
    Also, x_vector is as above.
    Here y should be 0, 1, or 2, depending on which class of
    irises the example belongs to.
    Learning is specified by alpha.
    """
    check = classify(W, x_vector)
    for i in range(0, 3):
        if y == i and check != y:
            for j in range(0, len(x_vector)):
                W[y][j] = W[y][j] + alpha * x_vector[j]
                W[check][j] = W[check][j] - alpha * x_vector[j]
            W[y][-1] += alpha
            W[check][-1] -= alpha
            return W, True
    return W, False


WEIGHTS = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
ALPHA = 1.0


def train_for_an_epoch(training_data, reporting=True):
    """Go through the given training examples once, in the order supplied,
    passing each one to train_with_one_example.
    Return the weight vector and the number of weight updates.
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


# THIS MAY BE HELPFUL DURING DEVELOPMENT:
TEST_DATA = [
    [20, 25, 1, 1, 0],
    [-2, 7, 2, 1, 1],
    [1, 10, 1, 2, 1],
    [3, 2, 1, 1, 2],
    [5, -2, 1, 1, 2]]


def test():
    print("Starting test with 3 epochs.")
    for i in range(10):
        train_for_an_epoch(TEST_DATA)
    print("End of test.")
    print("WEIGHTS: ", WEIGHTS)


if __name__ == '__main__':
    test()
