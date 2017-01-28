from flask import Flask
from flask import request

from hardware.robot.step import request_step


app = Flask(__name__)

@app.route("/status", methods=['POST'])
def run_step_when_ready():
    ## Request step will tell the robot to move to
    ## to its next location when both motors request the step.
    ## (i.e. they are ready)
    return request_step(request.form.motor_id)

@app.route("/test", methods=['POST'])
def test():
    print("Received request from MOTOR")
    return {response: "Hello!"}

if __name__ == "__main__":
    app.run(host='0.0.0.0')
