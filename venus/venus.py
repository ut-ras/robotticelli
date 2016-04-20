
import argparse
import numpy as np
import collections

import rounds as round_solver

def main():
    parser = argparse.ArgumentParser('venus')
    parser.add_argument('-l', '--labels', type=str, required=True)
    parser.add_argument('-s', '--slots', type=int, required=True)

    args = parser.parse_args()
    labels = np.load(args.labels)
    rounds = round_solver.solve_rounds(labels, args.slots)

    print(rounds)


if __name__ == '__main__':
    main()
