from flask import Flask
from flask import request
from flask import jsonify
from conf import MAX_ENCODER_STEPS
from conf import PORT
import conf
from celery import Celery
import hardware.motor.run as pwm
from hardware.motor.modules.control import Control
from hardware.motor.modules.motor import Motor
from hardware.motor.modules.encoder import Encoder

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)



@celery.task
def async_run_step(encoder_steps, speed):
    pwm.run(encoder_steps, speed)

@app.route("/", methods=['POST'])
def run_step():

    controller = Control(Motor(*conf.MOTOR_PINS), Encoder(*conf.ENCODER_PINS));
    ## The encoder will measure how much line has been pulled in,
    ## once it has stepped [encoder_steps] time, the program will
    ## message the robot RPi that this motor is ready for instructions
    form = dict(request.form)
    if 'encoder_steps' in form: 
        encoder_steps = float(form['encoder_steps'][0])
        spin_speed    = float(form['speed'][0])
        ## Debugging purposes
        print("ENCODER STEPS: " + str(encoder_steps))
       	print("SPEED: " + str(spin_speed))
	pwm.run(controller, encoder_steps, spin_speed)
    else:
        print("Faulty request, encoder steps not found")

    return jsonify({"response": "Hello!"})

@app.route("/test", methods=['POST'])
def test():
    print("Received test from ROBOT")
    return jsonify({"response": "Hello!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
