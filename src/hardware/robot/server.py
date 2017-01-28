from flask import Flask
from flask import request
from flask import jsonify

from hardware.robot.step import request_step


app = Flask(__name__)

@app.route("/status", methods=['POST'])
def run_step_when_ready():
    ## Request step will tell the robot to move to
    ## to its next location when both motors request the step.
    ## (i.e. they are ready)
    request_step(request.form.motor_id)
    return jsonify({response: "Success!"})

@app.route("/test", methods=['POST'])
def test():
    print("Received request from MOTOR")
    return jsonify({response: "Hello!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
