import RPIO.GPIO as GPIO

class Servo_PWM:
    '''
        Class for controlling a DC Servo with PWM,
        requires two pins per motor to function.
        Meant to be interfaced with a motor controller
    '''

    forward = None

    def __init__(self, fwd, back, rate=50):
        '''
            Starts PWM on the fwd pin and
            back pin, with a rate of [rate]
            hertz. Initializes to 0 duty cycle
        '''

        ## Initializing fwd and back pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(fwd, GPIO.OUT)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(back, GPIO.OUT)

        ## Exporting them to class variables so that
        ## they can be used by other functions
        self.forward  = GPIO.PWM(fwd, rate)
        self.backward = GPIO.PWM(back, rate)

        self.forward.begin(10)
        self.backward.begin(10)

    def changeDutyCycle(duty_cycle):
        '''
            Changes the duty cycle of a servo. [duty_cycle] is a
            float between 0 and 180, with 0 representing
            fully backwards, and 180 representing fully
            forwards
        '''
        if duty_cycle < 0 or duty_cycle > 180:
            raise ValueError('Speed must be between 0 and 180 inclusive')

        ## There is some overlap between the two PWM channels
        forward_duty_cycle  = max(0, speed - 80)

        self.forward.ChangeDutyCycle(forward_duty_cycle)

    def stop():
        self.forward.stop()

    def start():
        self.forward.start(10)
