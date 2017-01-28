import conf

from hardware.robot.com import test_connection
from hardware.robot.server import *

def main():
	if conf.LMOTOR_IP != '0.0.0.0':
		test_connection(conf.LMOTOR_IP)

	if conf.RMOTOR_IP != '0.0.0.0':
		test_connection(conf.RMOTOR_IP)
		
	app.run(host='0.0.0.0')
