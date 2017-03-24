import conf

from modules.com import send_ready
from modules.control import Control
from modules.motor import Motor
from modules.encoder import Encoder


## create a DC motor PWM output on pins 0, 1
## 0 controls forwards, 1 controls backwards
CONTROLLER = Control(Motor(*conf.MOTOR_PINS), Encoder(*conf.ENCODER_PINS))

def run(needed_encoder_steps, speed):
    direction = 0 if speed > 0 else 1
    speed = abs(speed)
    CONTROLLER.travelSpeedAndDir(needed_encoder_steps, (speed * 15 + 15), direction)
    print('completed task')
    #Reset for next run
    send_ready() # for robot

if __name__ == '__main__':
    import argparse
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("encoder_steps")
    PARSER.add_argument("spin_speed")
    ARGS = PARSER.parse_args()
    run(float(ARGS.encoder_steps), float(ARGS.spin_speed))

    
