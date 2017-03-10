import pigpio
import thread
from time import sleep

import conf
from conf import MAX_ENCODER_STEPS

from hardware.motor.modules.com import send_ready

## create a DC motor PWM output on pins 0, 1
## 0 controls forwards, 1 controls backwards


def run(controller, needed_encoder_steps, speed):

    direction = speed > 0 and 0 or 1
    speed = abs(speed)
    print(speed) 
    controller.travelSpeedAndDir(needed_encoder_steps, (speed * 15 + 15), direction)
    print('completed task')
    #Reset for next run
    send_ready() # for robot

