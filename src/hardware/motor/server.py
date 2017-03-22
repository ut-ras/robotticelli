import os
from flask import Flask, request, jsonify
from conf import MAX_ENCODER_STEPS, PORT
import hardware.motor.run as pwm

app = Flask(__name__)

@app.route("/", methods=['POST'])
def run_step():

    ## The encoder will measure how much line has been pulled in,
    ## once it has stepped [encoder_steps] time, the program will
    ## message the robot RPi that this motor is ready for instructions
    form = dict(request.form)
    if 'encoder_steps' in form: 
        encoder_steps = form['encoder_steps'][0]
        spin_speed    = form['speed'][0]
        ## Debugging purposes
        print("ENCODER STEPS: " + encoder_steps)
       	print("SPEED: " + spin_speed)
        ## Executes run.py outside of the context of flask to avoid bugs
        ## TODO: Revisit and make this code nicer
	    os.system("python run.py {} {}", encoder_steps, spin_speed)
    else:
        print("Faulty request, encoder steps not found")

    return jsonify({"response": "Hello!"})

@app.route("/test", methods=['POST'])
def test():
    print("Received test from ROBOT")
    return jsonify({"response": "Hello!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
