import pigpio
import thread
from time import sleep

from conf import MAX_ENCODER_STEPS
from hardware.motor.modules.motor import Motor_PWM
from hardware.motor.modules.encoder import Encoder
from hardware.motor.modules.com import send_ready

## create a DC motor PWM output on pins 0, 1
## 0 controls forwards, 1 controls backwards
motor = Motor_PWM(12, 13)
encoder = Encoder(13, 14)

def run(needed_encoder_steps, spin_turn_ratio):
    global motor
    global encoder

    direction = 0
    encoder_total_steps = 0
    motor.changeSpeedAndDir(100 * (1 +  spin_turn_ratio), direction)
    #while encoder_total_steps < abs(needed_encoder_steps):
    #   print(encoder)
    #   encoder_total_steps = encoder.readSteps()
    print('blam zam')
    sleep(1)
    print('zam blam')
    #TODO: change this algorithm to work with kalman filter and PID
    #Motionless
    motor.changeSpeed(90)
    #Reset for next run
    encoder.resetSteps()
    send_ready()

def testMotor():

