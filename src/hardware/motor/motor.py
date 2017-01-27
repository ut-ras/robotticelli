import pigpio as gpio

class Motor_PWM:
    '''
        Class for controlling a DC motor with PWM,
        requires two pins per motor to function.
        Meant to be interfaced with a motor controller
    '''

    ## Pin numbers for the two IO pins in use
    forward = None
    backward = None

    def __init__(self, fwd, back, rate=100000):
        '''
            Starts PWM on the fwd pin and
            back pin, with a rate of [rate]
            hertz. Initializes to 0 duty cycle
        '''

        ## Exporting them to class variables so that
        ## they can be used by other functions
        self.forward  = fwd
        self.backward = back

        ## Turn fwd and back into output pins
        gpio.set_mode(fwd, gpio.OUTPUT)
        gpio.set_mode(back, gpio.OUTPUT)

        ## Initializing pins to operate at [rate] frequency
        gpio.set_PWM_frequency(fwd, rate)
        gpio.set_PWM_frequency(back, rate)

        ## Initializing the motor to the equivalent of no speed
        gpio.set_PWM_dutycycle(fwd, 0)
        gpio.set_PWM_dutycycle(back, 0)

        ## Change scale of speed from 0-512 to 0-180
        gpio.set_PWM_range(fwd, 90)
        gpio.set_PWM_range(back, 90)

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
        gpio.set_PWM_dutycycle(fwd, forward_duty_cycle)
        gpio.set_PWM_dutycycle(back, backward_duty_cycle)

    def stop():
        '''Stops PWM at the pins but leaves the daemon running'''
        this.changeSpeed(0);
