import conf

os.system("pigpiod")

from hardware.motor.com import test_connection
from hardware.motor.server import *
from hardware.motor.motor import Motor_PWM

## Initialize motors, testing
motor = Motor_PWM(12, 13)
motor.changeSpeed(00)


def main():
	if conf.ROBOT_IP != '0.0.0.0':
		test_connection(conf.ROBOT_IP)

	app.run(host='0.0.0.0')
