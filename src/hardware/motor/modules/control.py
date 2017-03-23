from time import sleep

class Control:
    time_step = None
    motor = None
    encoder, error = None, None

    def __init__(self, Motor, Encoder, time_step=.01):
        self.motor = Motor
        self.encoder = Encoder
        self.error = 0
        self.time_step = time_step

    def travelSpeedAndDir(self, total_needed_steps, speed, mDir):
        '''
        Scales the motor speed between 15 and 40.
        0 maps to zero. Uses encoder steps to ramp up and down.
        '''
        TIME_STEP = self.time_step
        encoder_total_steps = 0
        self.motor.changeSpeedAndDir(0, mDir)
        print(speed, mDir, self.error)
        while abs(encoder_total_steps) < abs(total_needed_steps + self.error):
            sleep(TIME_STEP)

            encoder_total_steps += self.encoder.read_steps()
            # Assuming uniform acceleration
            expected_stop_distance = self.motor.current_speed**2 / 1000.0
            if expected_stop_distance > total_needed_steps - encoder_total_steps:
                break
            if int(total_needed_steps) == 0:
                break
            if mDir == 1:
                expected_stop_distance *= 2

            # Manaully ramps up, so that it can be
            # broken out of easily
            print(self.motor.currentDirection, encoder_total_steps)
            if self.motor.current_speed <= round(speed):
                self.motor.increment_speed(1)

        self.motor.changeSpeedAndDir(0, 0)
      # Motor speed ramping occurs on same thread,
        # so this is guaranteed to execute after stopping
        encoder_total_steps += self.encoder.read_steps()
        print(encoder_total_steps)
        self.error = total_needed_steps - encoder_total_steps
