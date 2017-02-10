import httplib
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

def test_connection(to_ip):
    try:
        '''
            This is to test the connection with the RPI center
            module
        '''
        status  = urllib.urlencode({'from': conf.IP[conf.MODE]})
        conn = httplib.HTTPConnection(to_ip, port=conf.PORT);
        conn.request("POST", "/test", status)
        content = conn.getresponse()
        conn.close()
        return True
    except:
        return False
        print("not reached")
