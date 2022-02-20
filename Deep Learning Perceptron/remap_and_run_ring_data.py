"""remap_and_run_ring_data.py

Fill out this file, copying code as needed from run_ring_data.py.
Write code to import remapper,
and use that for remapping the ring data after it has been read in.
Then train your binary perceptron on the remapped data,
and examine the plot of the data and the separating line.

YOUR NAME: Sheng Yu

"""

import binary_perceptron
import remapper
import csv
from matplotlib import pyplot as plt

X_MIN = 0
X_MAX = 0


def plot_2d_points(points_to_plot, marker='o', more_coming=True):
    """Here points_to_plot is a list of triples of the form [xi, yi, ci]
    where ci is either -1 or +1.
    """
    global X_MIN, X_MAX
    xpoints = [pt[0] for pt in points_to_plot]
    X_MIN = min(xpoints)
    X_MAX = max(xpoints)
    plt.figure(figsize=(8, 8))
    ypoints = [pt[1] for pt in points_to_plot]
    classes = ['o:r' if pt[2] == -1 else 'P:b' for pt in points_to_plot]
    for (x, y, c) in zip(xpoints, ypoints, classes):
        plt.plot(x, y, c, linestyle='')
    if more_coming: return
    plt.show()


PLOTLINE_COUNT = 1


def plot_separator(w0, w1, w2):
    """Add to the plot so far a line that best represents
    the current set of weights, where we are interpreting
    them as w0*x + w1*y + w2 = 0.
    x
    """
    global X_MIN, X_MAX, PLOTLINE_COUNT
    y1 = (-w2 - w0 * X_MIN) / w1
    y2 = (-w2 - w0 * X_MAX) / w1
    plt.plot([X_MIN, X_MAX], [y1, y2], label='{i}'.format(i=PLOTLINE_COUNT))
    PLOTLINE_COUNT += 1
    plt.legend(loc='best')


TRAINING_DATA = []
TESTING_DATA = []


def read_data():
    global TRAINING_DATA
    data_as_strings = list(csv.reader(open('ring-data.csv'), delimiter=','))
    print("data_as_strings:")
    print(data_as_strings)
    temp = []
    for value in data_as_strings:
        x = float(value[0])
        y = float(value[1])
        c = int(value[2])
        x, y = remapper.map(x, y)
        temp.append([x, y, c])
    TRAINING_DATA = temp


read_data()
plot_2d_points(TRAINING_DATA)

N_EPOCHS = 20

for i in range(N_EPOCHS):
    changed_count = binary_perceptron.train_for_an_epoch(TRAINING_DATA)
    if changed_count == 0:
        break
    plot_separator(*binary_perceptron.WEIGHTS)

print("TRAINING IS DONE")

plt.show()
