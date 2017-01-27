import RPi.GPIO as GPIO

class Servo_PWM:
    '''
        Class for controlling a servo with PWM,
        requires two pins per motor to function.
        Meant to be interfaced with a motor controller
    '''

    forward = None

    def __init__(self, fwd, rate=500):
        '''
            Starts PWM on the fwd pin and
            back pin, with a rate of [rate]
            hertz. Initializes to 0 duty cycle
        '''

        ## Initializing fwd and back pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(fwd, GPIO.OUT)

        ## Exporting them to class variables so that
        ## they can be used by other functions
        self.forward = GPIO.PWM(fwd, rate)
        self.forward.begin(0)

    def changeDutyCycle(duty_cycle):
        '''
            Changes the duty cycle of a servo. [duty_cycle] is a
            float between 0 and 180, with 0 representing
            fully backwards, and 180 representing fully
            forwards
        '''
        if duty_cycle < 0 or duty_cycle > 100:
            raise ValueError('Speed must be between 0 and 100 inclusive')

        ## There is some overlap between the two PWM channels
        self.forward.ChangeDutyCycle(duty_cycle)

    def stop():
        self.forward.stop()

    def start():
        self.forward.start(0)
