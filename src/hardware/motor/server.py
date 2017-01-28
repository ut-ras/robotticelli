from flask import Flask
from flask import request
from flask import jsonify
from conf import MAX_ENCODER_STEPS
import hardware.motor.pwm


app = Flask(__name__)

@app.route("/", methods=['POST'])
def run_step():
    ## The encoder will measure how much line has been pulled in,
    ## once it has stepped [encoder_steps] time, the program will
    ## message the robot RPi that this motor is ready for instructions
    print(request.form)
    encoder_steps = MAX_ENCODER_STEPS * request.form.turn_ratio

    #pwm.run(encoder_steps)

    return jsonify({"response": "Hello!"})

@app.route("/test", methods=['POST'])
def test():
    print("Received request from MOTOR")
    return jsonify({"response": "Hello!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
