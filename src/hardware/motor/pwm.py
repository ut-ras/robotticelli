from .motor import Motor_PWM
from .conf import MAX_ENCODER_STEPS

encoder_total_steps = 0

## create a DC motor PWM output on pins 0, 1
## 0 controls forwards, 1 controls backwards
motor = Motor_PWM(0,1)

def run(encoder_steps):
    direction = 0;
    if encoder_total_steps < 0:
        direction = -1
    elif encoder_total_steps > 0:
        direction = 1;

    ##TODO: implement turning, track encoder_total_steps
