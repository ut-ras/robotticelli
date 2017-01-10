import numpy as np

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
	#to be implemented

def main():
	print transform((3,1), (1,2), (9,8))

if __name__ == '__main__':
	main()
