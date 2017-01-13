from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/action", method=['POST'])
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(port='0.0.0.0')
