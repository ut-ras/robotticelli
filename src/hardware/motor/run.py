import conf

from .modules.com import send_ready
from .modules.control import Control
from .modules.motor import Motor
from .modules.encoder import Encoder


## create a DC motor PWM output on pins 0, 1
## 0 controls forwards, 1 controls backwards
controller = Control(Motor(*conf.MOTOR_PINS), Encoder(*conf.ENCODER_PINS));

def run(controller, needed_encoder_steps, speed):
    direction = speed > 0 and 0 or 1
    speed = abs(speed)
    print(speed) 
    controller.travelSpeedAndDir(needed_encoder_steps, (speed * 15 + 15), direction)
    print('completed task')
    #Reset for next run
    send_ready() # for robot

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("encoder_steps")
    parser.add_argument("spin_speed")
    args = parser.parse_args()

