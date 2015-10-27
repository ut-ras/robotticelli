
import argparse
import numpy as np
import collections


def find_round(labels, slots=(0, 1, 2, 3)):
    labels = np.pad(labels, ((0, 0), (len(slots), 0)), mode='edge')
    # labels = labels.reshape((labels.shape[0], labels.shape[1], 1))

    # TODO: replace with numpy stuff
    labels2 = np.empty((labels.shape[0], labels.shape[1], len(slots)), dtype="bool")
    for y in range(labels.shape[0]):
        for x in range(labels.shape[1]):
            labels2[y][x] = np.array([
                True if i == labels[y][x] else False
                for i in slots]).astype("bool")

    labels = labels2

    for y in range(labels.shape[0]):
        for x in range(len(slots), labels.shape[1]):
            val = labels[y][x]
            for v in range(1, len(slots)):
                labels[y][x - v][v] |= labels[y][x][v]
                labels[y][x][v] = 0

    print(labels)



def main():
    parser = argparse.ArgumentParser('venus')
    parser.add_argument('-l', '--labels', type=str, required=True)
    parser.add_argument('-s', '--slots', type=int, required=True)

    args = parser.parse_args()
    labels = np.load(args.labels)
    find_round(labels, slots=range(args.slots))


if __name__ == '__main__':
    main()
