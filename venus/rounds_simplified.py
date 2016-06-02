import numpy as np 
import time
from scipy.spatial.distance import cdist



def find_nearest_neighbor(coordinate, coordinate_list):
	neighbor_distances = cdist([coordinate], coordinate_list)
	nn_idx = np.argmin(neighbor_distances)

	return coordinate_list[nn_idx][:], nn_idx;

## TODO: Implement Christofide's Heuristic for find_short_path
def find_short_path(coordinate_list):
	path = []
	coordinate_list = list(coordinate_list)

	if len(coordinate_list) == 0:
		raise("coordinate list empty")

	## Copies first element into new array
	nearest_neighbor, nn_idx = coordinate_list[0][:], 0;

	## Removes from list so no-self matching occurs
	del coordinate_list[nn_idx]
	path.append(nearest_neighbor)

	for _ in range(len(coordinate_list)):

		nearest_neighbor, nn_idx = find_nearest_neighbor(nearest_neighbor, coordinate_list);

		del coordinate_list[nn_idx]
		path.append(nearest_neighbor)


	return path + coordinate_list

def solve_rounds(pixels, max_pixels_per_can=100):
	output = []

	## "Straining" pixels by value
	picture_mod   = pixels.shape[0]

	pixels = pixels.reshape(pixels.size, 1)
	unique = np.unique(pixels)

	for unique_value in unique:
		filtered_idx = np.where(pixels == unique_value)

		x_coords = np.remainder(filtered_idx[0], picture_mod)
		y_coords = np.floor_divide(filtered_idx[0], picture_mod)

		coords   = np.transpose([x_coords, y_coords])

		## Ordering pixels

		ordered = np.array(find_short_path(coords))
		order_s = ordered.shape[0]

		num_divisions = int(order_s/max_pixels_per_can) + 1

		if num_divisions > 0:
			split_points  = [i*max_pixels_per_can for i in range(num_divisions)]
			output.append(np.array_split(ordered, split_points)[1:])
		else:
			output.append(ordered)


	print(output)


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


solve_rounds(np.array(sample), 10)

