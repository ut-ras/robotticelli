import numpy as np
from settings import *

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
	return transform([-x, H - y], [W - x, H - y], vec)

def get_motor_spin_ratio(x, y, vec):
	'''
	Gives ratio of top left motor to top right motor using our solved input
	Negative is out, positive is in
	'''
	res = xytransform(x, y, vec)
	return res/(max(abs(res[0]),abs(res[1])) or 1)

def main():
	print(get_motor_spin_ratio(10, 5, (1,0)))

if __name__ == '__main__':
	main()