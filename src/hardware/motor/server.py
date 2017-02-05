from flask import Flask
from flask import request
from flask import jsonify
from conf import MAX_ENCODER_STEPS
import hardware.motor.pwm as pwm
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route("/", methods=['POST'])
def run_step():
    ## The encoder will measure how much line has been pulled in,
    ## once it has stepped [encoder_steps] time, the program will
    ## message the robot RPi that this motor is ready for instructions
    form = dict(request.form)
    #Extracts the turn ratio from the form being sent
    encoder_steps = MAX_ENCODER_STEPS * float(form['turn_ratio'][0])
    print("TURN RATIO: " + form['turn_ratio'][0])
    print("ENCODER STEPS: " + str(encoder_steps))
    pwm.run(encoder_steps)

    return jsonify({"response": "Hello!"})

@app.route("/test", methods=['POST'])
def test():
    print("Received request from MOTOR")
    return jsonify({"response": "Hello!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
