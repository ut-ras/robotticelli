import argparse
import os
from time import sleep

from modules.motor import Motor_PWM

my_motor = Motor_PWM(18, 17, 4, 27, 23, 24)
parser = argparse.ArgumentParser()
parser.add_argument('strings', metavar='S',type=str,nargs='+')

duty_cycles = parser.parse_args().strings[0]

for i in duty_cycles.split():
	speed = abs(int(i))
	mdir = (0 if int(i) >= 0 else 1)
	print(mdir)
	my_motor.changeSpeedAndDir(speed, mdir)
	sleep(3)
my_motor.changeSpeedAndDir(0, 0)
