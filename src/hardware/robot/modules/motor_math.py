import numpy as np
from conf import *
from numpy.linalg import norm
## Generates turn ratios for motors

def transform(r1, r2, vec):
	'''
	Performs a basis transform given two new basis vectors, r1 and r2
	'''
	return np.linalg.solve(
		np.array([[r1[0], r2[0]], [r1[1], r2[1]]]),
		np.array(vec)
	)

def xytransform(x, y, vec):
	'''
	Finds r1 and r2 based on x,y and then does a basis transform of vec
	'''
	to_top_left = [-x, H - y]
	to_top_right = [W - x, H - y]
	dir_to_top_left = to_top_left/norm(to_top_left)
	dir_to_top_right = to_top_right/norm(to_top_right)
	return transform(dir_to_top_left, dir_to_top_right, vec)

def get_motor_spin_capped(x, y, vec):
	'''
	Gives ratio of top left motor to top right motor using our solved input
	Negative is out, positive is in
	'''
	res = xytransform(x, y, vec)
	print("transform result: " + str(res))
	## this normalizes the result for the biggest number.
	biggest_step = max(abs(res[0]), abs(res[1]))
	if biggest_step > DISTANCE_PER_STEP * MAX_ENCODER_STEPS:
		print("Distance too big to cover... scaling")
		return MAX_ENCODER_STEPS * res/(biggest_step or 1)
	else:
		return res/DISTANCE_PER_STEP

def main():
	print(get_motor_spin_ratio(10, 5, (1,0)))

if __name__ == '__main__':
	main()
