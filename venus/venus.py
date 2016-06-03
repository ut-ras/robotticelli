
import argparse
import numpy as np
import collections

import rounds as round_solver

from calc_angles import adjust

def main():
	parser = argparse.ArgumentParser('venus')
	#parser.add_argument('-l', '--labels', type=str, required=True)
	parser.add_argument('-s', '--slots',  type=int, default =4)
	parser.add_argument('-p', '--pixels', type=int, default =100)
	parser.add_argument('-w', '--write',  type=str, required=True)

	sample = [
	    [9, 9, 9, 9, 9, 1, 0, 9],
	    [9, 9, 9, 9, 9, 1, 0, 0],
	    [9, 9, 9, 9, 1, 1, 1, 1],
	    [9, 9, 0, 1, 1, 9, 1, 9],
	    [0, 0, 1, 1, 9, 9, 9, 9],
	    [9, 9, 0, 9, 9, 0, 0, 0],
	    [9, 9, 9, 9, 9, 0, 0, 0],
	    [9, 9, 9, 9, 9, 1, 1, 1]
	]

	args = parser.parse_args()
	#labels = np.load(args.labels)
	rounds = round_solver.solve_rounds(sample, args.pixels)

	output = open(args.write, "w")

	## CREATING INSTRUCTIONS
	can_number = 0
	for colors in rounds:
		output.write("\nLABEL " + str(colors[0]) + "\n")
		for path in colors[1:]:
			for point in path:
				point = adjust(point, can_number)
				output.write(str(can_number) + " - (" + str(point[0]) + "," + str(point[1]) + ")\n")

			can_number = (can_number + 1) % args.slots

			if can_number == 0:
				output.write("\nSTOP\n")

if __name__ == '__main__':
    main()
