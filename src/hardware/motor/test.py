import argparse
import os

from modules.motor import Motor_PWM

os.exec("pigpiod -s 1")

my_motor = Motor_PWM(18, 17, 4, 27, 23, 24)
parser = argparse.ArgumentParser()
parser.add_argument('integers', metavar='N',type=int,nargs='+')

duty_cycle = parser.parse_args().integers[0]

my_motor.changeSpeedAndDir(duty_cycle, 0)
