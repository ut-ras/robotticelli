import os
# import conf
from time import sleep
import random

from hardware.motor.modules.motor import Motor
from modules.encoder import Encoder
from modules.control import Control

my_motor = Motor(*conf.MOTOR_PINS)
my_controls = Control(my_motor, Encoder(*conf.ENCODER_PINS));

distance = random.randint(15, 45)
velocity = 20

speed = abs(velocity)
mdir = velocity < 0


while 1:
	my_controls.travelSpeedAndDir(int(distance), speed, mdir)
	sleep(1)
	my_controls.travelSpeedAndDir(int(distance), speed, not mdir)
	sleep(1)
