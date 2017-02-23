import pigpio
import threading
from time import sleep

class Motor_PWM:
    '''
        Class for controlling a DC motor with PWM,
        requires two pins per motor to function.
        Meant to be interfaced with a motor controller
    '''

    ## Pin numbers for the two IO pins in use
    forward = None
    direction = None
    reset = None
    currentSense = None
    fault1 = None
    fault2 = None
    pi = None

    currentSpeed = None
    currentDirection = None

    lock = threading.Lock()

    def __init__(self, fwd, pDir, res, CS, FF1, FF2, rate=20000):
        '''
            Starts PWM on the fwd pin and
            back pin, with a rate of [rate]
            hertz. Initializes to 0 duty cycle.
            Needs access to the pigpio daemon,
            achieved by passing the pi parameter
            through
        '''

        ## Exporting them to class variables so that
        ## they can be used by other functions
        self.forward  = fwd
        self.direction = pDir
        self.reset = res
        self.currentSense = CS
        self.fault1 = FF1
        self.fault2 = FF2
        self.pi = pigpio.pi()
	self.currentSpeed = 0
	self.currentDirection=0

        ## Turn fwd and direction into output pins
        self.pi.set_mode(fwd, pigpio.OUTPUT)
        self.pi.set_mode(pDir, pigpio.OUTPUT)
        self.pi.set_mode(res, pigpio.OUTPUT)

        ## Turn current sense and fault pins into input pins
        self.pi.set_mode(FF1, pigpio.INPUT)
        self.pi.set_mode(FF2, pigpio.INPUT)
        self.pi.set_mode(CS, pigpio.INPUT)

        ## Initializing fault interrupts
        self.pi.callback(FF1, pigpio.RISING_EDGE, self.fault)
        self.pi.callback(FF2, pigpio.RISING_EDGE, self.fault)

        ## Initializing pins to operate at [rate] frequency
        self.pi.set_PWM_frequency(fwd, rate)

        ## Initializing the motor to the equivalent of no speed
        self.pi.set_PWM_dutycycle(fwd, 0)

        ## Change scale of speed from 0-512 to 0-180
        self.pi.set_PWM_range(fwd, 100)

    def lerp_speed(self, speed):
        '''
	     Smoothly changes speed from one to another by
	     using linear interpolation
	'''
	currentSpeed = self.currentSpeed
        if currentSpeed > speed:
	    for i in range(currentSpeed, speed, -1):
	    	self.pi.set_PWM_dutycycle(self.forward, i)
		sleep(0.01)
	    self.currentSpeed = speed

    def changeSpeedAndDir(self, speed, mDir):
        '''
            Changes the speed and direction of a motor. [speed] is a
            float between 0 and 100. [pDir] is the direction of power
            flow on the motor making it go forward or backward
        '''
        if speed < 0 or speed > 100:
            raise ValueError('Speed must be between 0 and 100 inclusive')

        ## Adjusting PWM to match calculated duty cycles
	self.lock.acquire()

	## TODO: Encoder callback to make more threadsafe
        ## Setting the direction of the motor
	if self.currentDirection != mDir:
		self.lerp_speed(speed)
		self.pi.write(self.direction, mDir)
		self.currentDirection = mDir
	lerp_speed(speed)

	self.lock.release()

    def stop(self):
        '''Stops PWM at the pins but leaves the daemon running'''
        self.pi.changeSpeed(0);

        ## Changes motor driver to low energy mode
        self.write(self.reset, 0)

    def fault(self):
        ## detects fault, stops motor, and notes which fault occurred
        '''Detected fault '''
        if self.fault1 and self.fault2:
            print "Detected fault under voltage"
        elif self.fault1:
            print "Detected fault overtemp"
        elif self.fault2:
            print "Detected fault short circuit"
        stop(self)

