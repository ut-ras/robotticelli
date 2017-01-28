class Encoder:
    '''
        Class for reading from the encoders attached
        to the winch. Requires two general purpose IO
        pins to be used on the Raspberry Pi
    '''

    ## TODO: IMPLEMENT ACTUAL ENCODER LOGIC
    total_steps = None
    def __init__(self, pin1, pin2):
        self.total_steps = 0


    def readSteps():
        self.total_steps += 1
        return self.total_steps

    def resetSteps():
        self.total_steps = 0
