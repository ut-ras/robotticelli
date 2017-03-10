import pigpio
from time import sleep

class Servo:
    servo_min = 900 # minimum pulsewidth, uS
    servo_max = 2100 # maximum pulsewidth, uS
    spray_angle = 90 #servo angle when can begins spraying
    stop_angle = 150 # servo angle when can stops spraying

    servo_pin = None

    pi = None
    def __init__(servo_pin = 17):
        self.pi = pigpio.pi()

    #map desired servo angle to pulsewidth
    def map(self, value, from_low, from_high, to_low, to_high):
        from_range   = from_high - from_low
        to_range     = to_high - to_low
        scale_factor = float(from_range)/to_range
        return to_low + (value/scale_factor)

    #command servo angle
    def set_angle(self, angle):
        pulse = map(angle, 0, 180, self.servo_min, self.servo_max)
        self.pi.set_servo_pulsewidth(self.servo_pin, pulse)

    #command servo to spray
    def press(self):
        self.set_angle(self.servo_pin, self.spray_angle)

    #command servo to stop spraying
    def release(self):
        self.set_angle(self.servo_pin, self.stop_angle)

    #spray for a set time limit
    def spray(self, time_spray = 3):
        self.press()
        sleep(time_spray)
        self.stop()
