from time import sleep
from hardware.motor.modules.motor import Motor
from hardware.motor.modules.encoder import Encoder

import conf

class Control:
	time_step = None
	motor = None
	encoder, error = None, None

	def __init__(self, time_step = .01):
		self.motor   = Motor(*conf.MOTOR_PINS)
		self.encoder = Encoder(*conf.ENCODER_PINS)
		self.error = 0
		self.time_step = time_step

	def travelSpeedAndDir(self, total_needed_steps, speed, mDir):
		'''
		Scales the motor speed between 15 and 40.
		0 maps to zero. Uses encoder steps to ramp up and down.
		''' 
		TIME_STEP = self.time_step
		
		self.motor.changeSpeedandDir(100 * abs(speed), direction)
		encoder_total_steps = 0

		while abs(encoder_total_steps) < abs(total_needed_steps + error):
			sleep(TIME_STEP)
			
			encoder_total_steps += self.encoder.readSteps()
			## Assuming uniform acceleration
			expected_stop_distance = motor.currentSpeed^2/200.0
			## Manaully ramps up, so that it can be
			## broken out of easily
			if self.motor.currentSpeed <= speed:
					 self.motor.incrementSpeed(1)

			if expected_stop_distance > total_needed_steps - encoder_total_steps:
					 break

		self.motor.changeSpeedAndDir(0, 0)
      ## Motor speed ramping occurs on same thread,
		## so this is guaranteed to execute after stopping
		encoder_total_steps += self.encoder.readSteps()
		self.error = total_needed_steps - encoder_total_steps
