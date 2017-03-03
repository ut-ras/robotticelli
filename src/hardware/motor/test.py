import argparse
import os
import conf
from time import sleep

from modules.control import Control

parser = argparse.ArgumentParser()
parser.add_argument('strings', metavar='S',type=str,nargs='+')
duty_cycles = parser.parse_args().strings[0]

my_controls = Control()
speed = abs(int(duty_cycles))
mdir = (0 if int(i) >= 0 else 1)

my_controls.travelSpeedAndDir(10, 20, 1)

