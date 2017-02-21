import argparse
import os
from time import sleep

from modules.motor import Motor_PWM

my_motor = Motor_PWM(18, 17, 4, 27, 23, 24)
parser = argparse.ArgumentParser()
parser.add_argument('integers', metavar='N',type=int,nargs='+')

duty_cycles = parser.parse_args().integers

for i in duty_cycles:
	speed = abs(i)
	mdir = (i >= 0 and 0 or 1)
	my_motor.changeSpeedAndDir(speed, mdir)
	sleep(3)
my_motor.changeSpeedAndDir(0, 0)
