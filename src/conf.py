#IP Destinations for robot components
LMOTOR_IP = '10.156.2.107'
RMOTOR   = '0.0.0.0'
ROBOT_IP = '10.156.0.221'

#String "LMOTOR", "RMOTOR", "ROBOT", or "SETUP"
MODE = 'ROBOT'

# Wall parameters
H  = 10   #Wall Height in m
W  = 20   #Wall Width in m
g  = 9.81 #Acceleration of gravity in m/s^2
m  = 10   #The robot mass in kg

h  = .5   #Robot height in m
w  = .5   #Robot width in m

bx = W * .1   #Buffer in meters between the edge of the wall and the edge of the mural
by = H * .1


# Motor step parameters
MAX_ENCODER_STEPS = 100
