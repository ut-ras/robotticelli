from time import sleep
from hardware.motor.modules.motor import Motor
from hardware.motor.modules.encoder import Encoder

import conf

motor = Motor(*conf.MOTOR_PINS)
encoder = Encoder(*conf.ENCODER_PINS)

def travelSpeedAndDir(self, total_needed_steps, speed, mDir):
        '''
		      Scales the motor speed between 15 and 40.
		  		0 maps to zero. Uses encoder steps to ramp up and down.
		  ''' 
        self.changeSpeedandDir(100 * abs(speed), direction)
        encoder_total_steps = 0
        TIME_STEP = .1
        while abs(encoder_total_steps) < abs(total_needed_steps):
            sleep(TIME_STEP)

            cycle_steps = self.encoder.readSteps()
            encoder_total_steps += cycle_steps
            recorded_speed = cycle_steps/TIME_STEP
            
				## Assuming constant ramping, the motor will stop speed^2/200
				## encoder steps after requesting to stop.
				##if recorded_speed^2 > 200*(total_needed_steps - encoder_total_steps):
				##	 break

        motor.changeSpeedAndDir(0)


