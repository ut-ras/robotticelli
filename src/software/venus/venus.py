
import argparse
import numpy as np
import collections

from .rounds import solve_rounds
from .calc_angles import map_to_wall

def main():
	parser = argparse.ArgumentParser('venus')
	parser.add_argument('-l', '--labels', type=str, required=True)
	parser.add_argument('-s', '--slots',  type=int, default =4)
	parser.add_argument('-p', '--pixels', type=int, default =100)
	parser.add_argument('-w', '--write',  type=str, required=True)

	args = parser.parse_args()

	venus(args.labels, args.slots, args.pixels, args.write)

## Rows with -1s everwhere that isn't the first spot indicate a COLOR change
def venus(labels, write, slots=4, pixels=100):
	if type(labels) == "String":
		labels = np.load(labels)

	rounds = solve_rounds(labels, pixels)
	output = open(write, "w")

	## CREATING INSTRUCTIONS
	can_number = 0
	for colors in rounds:
		output.write(str(colors[0]) + "\t-1\t-1\n")
		for path in colors[1:]:
			for point in path:
				point = map_to_wall(point, labels.shape, can_number)
				output.write(str(can_number) + "\t" + str(point[0]) + "\t" + str(point[1]) + "\n")

			can_number = (can_number + 1) % slots

if __name__ == '__main__':
    main()
