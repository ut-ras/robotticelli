import thread
from flask import Flask, request, jsonify
from celery import Celery

from hardware.robot.step import request_step

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def async_request_step(motor_id):
    request_step(motor_id)

@app.route("/status", methods=['POST'])
def run_step_when_ready():
    ## Request step will tell the robot to move to
    ## to its next location when both motors request the step.
    ## (i.e. they are ready)
    form = dict(request.form)
    print("Received READY from " + form['motor_id'][0])
    async_request_step.delay(form['motor_id'][0])
    return jsonify({"response": "Success!"})

@app.route("/test", methods=['POST'])
def test():
    print("Received TEST request from MOTOR")
    return jsonify({"response": "Hello!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
