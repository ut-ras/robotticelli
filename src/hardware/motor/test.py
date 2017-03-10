import argparse
import os
import conf
from time import sleep

from modules.motor import Motor
from modules.encoder import Encoder
from modules.control import Control

my_controls = Control(Motor(*conf.MOTOR_PINS),Encoder(*conf.ENCODER_PINS));

parser = argparse.ArgumentParser()
parser.add_argument('strings', metavar='S',type=str,nargs='+')
args = parser.parse_args().strings[0].split()
distance = int(args[0])
velocity = int(args[1])

speed = abs(velocity)
mdir = velocity < 0


while 1:
	my_controls.travelSpeedAndDir(int(distance), speed, mdir)
	sleep(2)
	my_controls.travelSpeedAndDir(int(distance), speed, not mdir)
        sleep(2)
