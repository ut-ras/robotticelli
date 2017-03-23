import conf
from .server import app
from .modules.com import test_connection
## Initialize motors, testing

def main():
    '''
		Entry point for the motor hardware. Waits until the other motors are ready to communicate,
		then bootstraps the needed processes and begins the server
	'''
    if conf.ROBOT_IP != '0.0.0.0':
        test_connection(conf.ROBOT_IP)

    app.run(host='0.0.0.0', port=conf.PORT)
