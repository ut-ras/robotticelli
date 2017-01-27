from hardware.motor.server import *
from hardware.motor.motor import Motor_PWM

## Initialize motors, testing
motor = Motor_PWM(12,13)
motor.changeSpeed(100)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
