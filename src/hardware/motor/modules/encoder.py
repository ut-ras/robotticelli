import pigpio
import threading
from time import sleep
class Encoder:
    '''
        Class for reading from the encoders attached
        to the winch. Requires two general purpose IO
        pins to be used on the Raspberry Pi
    '''

    pi = pigpio.pi()
    ## State of our system
    rotary_counter = 0;
    last_counter = 0;

    ## Encoder pin info
    pin_a = 0;
    pin_b = 0;

    ## Current vals being read on our encoder pins
    pin_a_val = 0;
    pin_b_val = 0;

    ## Used to lock system state changes so that add_event_detect doesn't
    ## conflicct with something like reset_steps
    lock = threading.Lock()

    def __init__(self, pin1, pin2):
        self.rotary_counter = 0
        self.pin_a = pin1

        self.pin_b = pin2

        self.pi.set_mode(self.pin_a, pigpio.INPUT)
        self.pi.set_mode(self.pin_b, pigpio.INPUT)

        self.pi.callback(self.pin_a, pigpio.RISING_EDGE, self.rotary_interrupt)
        self.pi.callback(self.pin_b, pigpio.RISING_EDGE, self.rotary_interrupt)

    def rotary_interrupt(self):
        new_a_val = self.pi.read(self.pin_a)
        new_b_val = self.pi.read(self.pin_b)

        ## If this function was fired and there is really no change
        if (self.pin_a_val == new_a_val and self.pin_b_val == new_b_val):
            return

        self.pin_a_val = new_a_val
        self.pin_b_val = new_b_val

        ## If both pins are high
        if (new_a_val and new_b_val):
            self.lock.acquire()

            if (pin == self.pin_b):
                self.rotary_counter += 1
            else:
                self.rotary_counter -= 1

            self.lock.release()

    ## Returns the number of steps since last read
    ## Resets steps in the process. This assures overflow protection.
    def read_steps(self):
        self.lock.acquire()

        num_steps = self.rotary_counter - self.last_counter
        self.reset_steps()

        self.lock.release()

        return num_steps

    ## Returns the number of steps since last read
    ## Doesn't reset steps, but updates the state of last_counter.
    def read_delta_steps(self):
        self.lock.acquire()

        num_steps = self.rotary_counter - self.last_counter
        self.last_counter = self.rotary_counter

        self.lock.release()
        return num_steps

    ## Reads the total counted steps since last reset
    def read_total_steps(self):
        return self.rotary_counter

    ## Steps all state counters to zero
    def reset_steps(self):
        self.rotary_counter = 0
        self.last_counter = 0
