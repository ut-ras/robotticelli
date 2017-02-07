#IP Destinations for robot components
LMOTOR_IP = '169.254.111.206'
RMOTOR_IP  = '0.0.0.0'
ROBOT_IP = '169.254.44.235'

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
DISTANCE_PER_STEP = .01 #Travel before encoder clicks in meters

## DO NOT TOUCH
IP = {
    'LMOTOR': LMOTOR_IP,
    'RMOTOR': RMOTOR_IP,
    'ROBOT': ROBOT_IP
}
