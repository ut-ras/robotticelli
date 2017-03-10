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
	Negative is out, positive is in. Needs to be used with gradient descent
	'''
	vec = (goal_x - x, goal_y - y)
	res = xytransform(x, y, vec)
	print("transform result: " + str(res))
	## this normalizes the result for the biggest number.
	biggest_step = max(abs(res[0]), abs(res[1]))
	if biggest_step > DISTANCE_PER_STEP * MAX_ENCODER_STEPS:
		print("Distance too big to cover... scaling")
		return MAX_ENCODER_STEPS * res/(biggest_step or 1)
	else:
		return res/DISTANCE_PER_STEP

##ABOVE CALCULATES VECTOR THEN TRANSFORMS TO NEW VECTOR SPACE
##BELOW TRANSFORMS TO NEW VECTOR SPACE THEN CALCULATES VECTOR

def triangulate(x, y):
   '''
   Takes an x, y on the wall and transforms it into an |r1|, |r2|
   (lengths as opposed to vectors in xytransform)
   '''
   to_top_left = np.linalg.norm([-x, H - y])
   to_top_right = np.linalg.norm([W - x, H - y])
	
   ## this normalizes the result for the biggest number.
   return to_top_left, to_top_right

def get_triangular_direction_vector(x, y, goal_x, goal_y):
   '''
	This is like get_motor_spin_capped but it will take the path of
	lowest tension rather than try to stick to a straight line. Also
	does not need to perform gradient decent to correctly hit target
	'''
   r_x, r_y = triangulate(x, y)
   r_goal_x, r_goal_y = triangulate(goal_x, goal_y)

   r_dx = r_goal_x - r_x
   r_dy = r_goal_y - r_y

   return (r_dx, r_dy)
	
def main():
	print(get_motor_spin_ratio(10, 5, (1,0)))

if __name__ == '__main__':
	main()
