import os
import time
import conf

from hardware.robot.modules.com import *
from hardware.robot.server import *
from hardware.robot.run import *

def main():
	pid = os.fork()
	## Executed in the new process
	print("Forking server")
	if pid == 0:
		app.run(host='0.0.0.0', port=5830)
	else:
		pid2 = os.fork()
		if pid2 == 0:
			if conf.LMOTOR_IP != '0.0.0.0':
				print("Waiting for LMOTOR ({0})".format(conf.LMOTOR_IP))

				while not test_connection(conf.LMOTOR_IP):
					print("waiting...")
					time.sleep(1)

				print("Successfully connected to LMOTOR")
			else:
				print("LMOTOR not configured... skipping.")

			if conf.RMOTOR_IP != '0.0.0.0':
				print("Waiting for RMOTOR ({0})".format(conf.RMOTOR_IP))

				while not test_connection(conf.RMOTOR_IP):
					print("waiting...")
					time.sleep(1)

				print("Successfully connected to RMOTOR")
			else:
				print("RMOTOR not configured... skipping.")

			print("Sending initial INSTRUCTION")
			request_step(0)
			print("------------------")
		else:
			print("Forking BACKGROUND worker")
			os.system("celery -A hardware.robot.server.celery worker --concurrency=1")
