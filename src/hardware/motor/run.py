import pigpio
import thread
from time import sleep

from conf import MAX_ENCODER_STEPS
from hardware.motor.modules.motor import Motor_PWM
from hardware.motor.modules.encoder import Encoder
from hardware.motor.modules.com import send_ready

## create a DC motor PWM output on pins 0, 1
## 0 controls forwards, 1 controls backwards
motor = Motor_PWM(18, 17, 4, 27, 23, 24)
encoder = Encoder(13, 14)

def run(needed_encoder_steps):
    global motor
    global encoder

    direction = 0
    encoder_total_steps = 0
    motor.changeSpeedandDir(100 * abs(needed_encoder_steps/MAX_ENCODER_STEPS), direction)
    #while encoder_total_steps < abs(needed_encoder_steps):
    #   print(encoder)
    #   encoder_total_steps = encoder.readSteps()
    print('blam zam')
    sleep(1)
    #TODO: change this algorithm to work with kalman filter and PID
    #Motionless
    motor.changeSpeedAndDir(90)
    #Reset for next run
    encoder.resetSteps()
    send_ready()

