import pigpio as pigpio

class Motor_PWM:
    '''
        Class for controlling a DC motor with PWM,
        requires two pins per motor to function.
        Meant to be interfaced with a motor controller
    '''

    ## Pin numbers for the two IO pins in use
    forward = None
    backward = None
    pi = None

    def __init__(self, pi, fwd, back, rate=100000):
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
        self.backward = back
        self.pi = pi

        ## Turn fwd and back into output pins
        pi.set_mode(fwd, gpio.OUTPUT)
        pi.set_mode(back, gpio.OUTPUT)

        ## Initializing pins to operate at [rate] frequency
        pi.set_PWM_frequency(fwd, rate)
        pi.set_PWM_frequency(back, rate)

        ## Initializing the motor to the equivalent of no speed
        pi.set_PWM_dutycycle(fwd, 0)
        pi.set_PWM_dutycycle(back, 0)

        ## Change scale of speed from 0-512 to 0-180
        pi.set_PWM_range(fwd, 90)
        pi.set_PWM_range(back, 90)

    def changeSpeed(speed):
        '''
            Changes the speed of a motor. [speed] is a
            float between 0 and 510, with 0 representing
            fully backwards, and 510 representing fully
            forwards
        '''
        if speed < 0 or speed > 180:
            raise ValueError('Speed must be between 0 and 510 inclusive')

        ## Deducing PWM duty cycles from speed given
        forward_duty_cycle  = max(0, speed - 90)
        backward_duty_cycle = max(0, 90 - speed)

        ## Adjusting PWM to match calculated duty cycles
        self.pi.set_PWM_dutycycle(fwd, forward_duty_cycle)
        self.pi.set_PWM_dutycycle(back, backward_duty_cycle)

    def stop():
        '''Stops PWM at the pins but leaves the daemon running'''
        this.changeSpeed(0);
