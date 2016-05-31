import numpy as np
from numpy import hypot as hyp
import matplotlib.pyplot as plt


H  = 10   #Wall Height in m
W  = 20   #Wall Width in m
g  = 9.81 #Acceleration of gravity in m/s^2
m  = 10   #The robot mass in kg

h  = .5   #Robot height in m
w  = .5   #Robot width in m

b  = W * .0001    #Buffer in meters between the edge of the wall and the edge of the mural   

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
	T3 = 0 * x/W 
	T4 = 0 - T3

	## Calculate other two tensions
	T1 = (m*g + T3*(tan2*cos3 - sin2) + T4*(tan2*cos4 - sin4))/(sin1 - tan2*cos1)
	T2 = (m*g + T3*(tan1*cos3 - sin3) + T4*(tan1*cos4 - sin4))/(sin2 - tan1*cos2)

	## Calculate the rotation of the robot
	phi_top = -(-h*T1*cos1 + w*T2*sin2 - h*T2*cos2 + w*T4*sin4 - .5*w*m*g)
	phi_bot = (-h*T1*sin1 - h*T2*sin2 - w*T2*cos2 - w*T4*cos4 + .5*h*m*g)

	angle = np.arctan(phi_top/phi_bot)

	print angle
	return [np.cos(angle), np.sin(angle)]

x_axis = np.linspace(b, W - b, 40)
y_axis = np.linspace(b, H - b, 40)


## For vector plot

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
