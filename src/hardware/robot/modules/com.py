import urllib
import conf
import requests
import os

##Module for communicating to the slaves.
##Wraps long HTTPRequests

def send_encoder_steps(to_ip, steps):
    '''
        This will let the main RPi module know
        that it is ready for the next motor
        instruction.
    '''
    headers = {"Content-type": "application/json"}
    status = {
        'from': conf.IP[conf.MODE],
        'encoder_steps': steps,
    }
    print(status)
    requests.post("http://{0}:{1}/".format(to_ip, conf.PORT), data=status)
    print("INSTRUCTION received by MOTOR at " + to_ip)

def send_encoder_steps_and_speed(to_ip, steps, speed):
    '''
        This will let the main RPi module know
        that it is ready for the next motor
        instruction.
    '''
    headers = {"Content-type": "application/json"}
    status = {
        'from': conf.IP[conf.MODE],
        'encoder_steps': steps,
		  'speed': speed,
    }
    print(status)
    requests.post("http://{0}:{1}/".format(to_ip, conf.PORT), data=status)
    print("INSTRUCTION received by MOTOR at " + to_ip)


def test_connection(to_ip):
    can_connect = True
    try:
        headers = {"Content-type": "application/json"}
        status = {
            'from': conf.IP[conf.MODE],
        }
        print(status)
        requests.post("http://{0}:{1}/test".format(to_ip, conf.PORT), data=status)
    except:
        can_connect = False

    return True
