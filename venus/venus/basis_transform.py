import numpy as np
import scipy
def basis_transform (r1, r2, dir):
	eq1 = [r1[0], r2[0]]
	eq2 = (r1[1], r2[1])
	a = np.array([eq1, eq2])
	x = np.array(dir)
	return np.linalg.solve(a, x)

def main():
	print basis_transform((3,1), (1,2), (9,8))

if __name__ == '__main__':
	main()