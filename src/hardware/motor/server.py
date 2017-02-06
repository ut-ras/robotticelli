from flask import Flask
from flask import request
from flask import jsonify
from conf import MAX_ENCODER_STEPS
from celery import Celery

import hardware.motor.run as pwm

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def async_run_step(encoder_step, turn_ratio):
    pwm.run(encoder_steps, turn_ratio)

@app.route("/", methods=['POST'])
def run_step():
    ## The encoder will measure how much line has been pulled in,
    ## once it has stepped [encoder_steps] time, the program will
    ## message the robot RPi that this motor is ready for instructions
    form = dict(request.form)
    if 'encoder_steps' in form:
        encoder_steps = round(float(form['encoder_steps'][0]))
        turn_ratio = float(form['turn_ratio'][0])
        ## Debugging purposes
        print("ENCODER STEPS: " + str(encoder_steps))
        async_run_step.delay(encoder_steps, turn_ratio)
    else:
        print("Faulty request, encoder steps not found")

    return jsonify({"response": "Hello!"})

@app.route("/test", methods=['POST'])
def test():
    print("Received test from ROBOT")
    return jsonify({"response": "Hello!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
