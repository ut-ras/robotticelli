import argparse
import os
import conf
from time import sleep

from modules.motor import Motor

my_motor = Motor(*conf.MOTOR_PINS)
my_encoder = Encoder(*conf.ENCODER_PINS)

parser = argparse.ArgumentParser()
parser.add_argument('strings', metavar='S',type=str,nargs='+')

duty_cycles = parser.parse_args().strings[0]

steps = 0

#my_motor.changeSpeedAndDir(10, 0)
#while steps < int(duty_cycles[0]):
#    steps += my_encoder.read_steps()
#    print(steps)
#    sleep(0.1)
#my_motor.changeSpeedAndDir(0, 0)
#
for i in duty_cycles.split():
	speed = abs(int(i))
	mdir = (0 if int(i) >= 0 else 1)
	print(mdir)
	my_motor.changeSpeedAndDir(speed, mdir)
	sleep(3)
my_motor.changeSpeedAndDir(0, 0)
