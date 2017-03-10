import pigpio
import thread
from time import sleep

import conf
from conf import MAX_ENCODER_STEPS
from hardware.motor.modules.control import Control
from hardware.motor.modules.motor import Motor
from hardware.motor.modules.encoder import Encoder
from hardware.motor.modules.com import send_ready

## create a DC motor PWM output on pins 0, 1
## 0 controls forwards, 1 controls backwards

controller = Control(Motor(*conf.MOTOR_PINS), Encoder(*conf.ENCODER_PINS));

def run(needed_encoder_steps, speed):
    global controller

    if needed_encoder_steps > 5:
        needed_encoder_steps = 5
    direction = speed > 0 and 0 or 1   
    controller.travelSpeedAndDir(needed_encoder_steps, (speed * 20 + 15), direction)
    #Reset for next run
    send_ready() # for robot

