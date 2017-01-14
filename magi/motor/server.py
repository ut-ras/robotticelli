from flask import Flask
from flask import request
from .conf import MAX_ENCODER_STEPS
import .pwm


app = Flask(__name__)

@app.route("/", method=['POST'])
def run_step():
    ## The encoder will measure how much line has been pulled in,
    ## once it has stepped [encoder_steps] time, the program will
    ## message the robot RPi that this motor is ready for instructions

    encoder_steps = MAX_ENCODER_STEPS * request.form.turn_ratio
    pwm.run(encoder_steps)

    return True

if __name__ == "__main__":
    app.run(port='0.0.0.0')
