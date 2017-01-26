from hardware.motor.motor import Motor_PWM
from hardware.motor.conf import MAX_ENCODER_STEPS
from hardware.motor.encoder import Encoder

encoder_total_steps = 0

## create a DC motor PWM output on pins 0, 1
## 0 controls forwards, 1 controls backwards
motor = Motor_PWM(0,1)

def run(encoder_steps):
    direction = 0
    encoder_total_steps = 0

    motor.changeSpeed(90 * (1 +  encoder_steps/MAX_ENCODER_STEPS))
    while encoder_total_steps < encoder_steps:
        encoder_total_steps = encoder.readSteps()

    #TODO: change this algorithm to work with kalman filter and PID  
    #Motionless
    motor.changeSpeed(90)
    #Reset for next run 
    encoder.resetSteps() 
