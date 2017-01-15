from flask import Flask
from flask import request


app = Flask(__name__)

@app.route("/", method=['POST'])

def run_step():
    return True

if __name__ == "__main__":
    app.run(host='0.0.0.0')
