import numpy as np
from numpy import hypot as hyp
import matplotlib.pyplot as plt
from settings import *

# numpy.linalg.solve
# numpy.solve
# numpy.linalg.inverse

H = float(H)
W = float(W)

## Calculates the direction of +X on the robot
def calc_angle(x, y):
	xp = W - x
	yp = H - y

	tan1 = -yp/x
	tan2 =  yp/xp
	tan3 =  y/x
	tan4 = -y/xp

	sin1 = yp/hyp(x , yp)
	sin2 = yp/hyp(xp, yp)
	sin3 = -y/hyp(x , y )
	sin4 = -y/hyp(xp, y )

	cos1 = -x/hyp(x , yp)
	cos2 = xp/hyp(xp, yp)
	cos3 = -x/hyp(x , y )
	cos4 = xp/hyp(xp, y )

	## Calculate dummy variables for tension
	T3 = 0 #m*g *(x/W)**2
	T4 = 0 #m*g - T3

	## Calculate other two tensions
	T1 = (m*g + T3*(tan2*cos3 - sin2) + T4*(tan2*cos4 - sin4))/(sin1 - tan2*cos1)
	T2 = (m*g + T3*(tan1*cos3 - sin3) + T4*(tan1*cos4 - sin4))/(sin2 - tan1*cos2)

	## Calculate the rotation of the robot
	phi_top = -(-h*T1*cos1 + w*T2*sin2 - h*T2*cos2 + w*T4*sin4 - .5*w*m*g)
	phi_bot =  (-h*T1*sin1 - h*T2*sin2 - w*T2*cos2 - w*T4*cos4 + .5*h*m*g)

	angle = np.arctan(phi_top/phi_bot)

	return [np.cos(angle), np.sin(angle)]


## Takes an pixel's Y coordinates and maps them to new coordinates along the wall
def map_to_wall(coordinate, size, can_number):

	## Robot layout:
	## RIGHT (-) [---1----2-XX-3----4---] LEFT (+)

	## XX marks this middle of the robot
	## #'s mark the can number

	x_center = coordinate[0]
	y_center = coordinate[1]

	x_size = size[0]
	y_size = size[1]

	## Maps the X,Y centers to the wall
	x_adjusted = (x_center * W - 2*bx)/x_size + bx
	y_adjusted = (y_center * H - 2*by)/y_size + by

	offset_direction = calc_angle(x_adjusted, y_adjusted)


	##Approximation of the can's holder size
	##Estimations will be replaced with
	##Measurements later.
	holder_len = w/4 - .05

	can_location_x = x_adjusted + holder_len*(can_number - 5/2)*offset_direction[0]
	can_location_y = y_adjusted - holder_len*(can_number - 5/2)*offset_direction[1]


	return [can_location_x, can_location_y]


if __name__ == "__main__":
	## For vector plot
	x_axis = np.linspace(bx, W - bx, 40)
	y_axis = np.linspace(by, H - by, 40)

	X, Y, EX, EY = [], [], [], []

	for x in x_axis:
		for y in y_axis:
			X.append(x)
			Y.append(y)
			EX.append(calc_angle(x, y)[0])
			EY.append(calc_angle(x, y)[1])
	plt.quiver(X,Y,EX,EY)

	## For heatmap

	# out = calc_angle(x_axis[:,None], y_axis[None,:])
	# plt.pcolor(out,cmap=plt.cm.Reds)

	plt.show()
