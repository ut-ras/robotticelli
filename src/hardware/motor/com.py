from __future__ import absolute_import
import httplib
import urllib
import conf
import requests

motor_id = -1
print(conf)

if conf.MODE == "LMOTOR":
    motor_id = 0
elif conf.MODE == "RMOTOR":
    motor_id = 1

## TODO: [low importance] MOVE ALL FUNCTIONS TO requests

## Motor functions for communicating with the master RPi.
## Filled with functions to wrap HTTP request code.

def send_ready(from_ip, to_ip):
    '''
        This will let the main RPi module know
        that it is ready for the next motor
        instruction.
    '''
    status = {
        'from': conf.IP[conf.MODE],
        'status': 'ready',
        'motor_id': motor_id
    }

    response = requests("http://{0}:5000/status".format(to_ip), data=status)
    print(response, response.text)

def test_connection(to_ip):
    try:
        '''
            This is to test the connection with the RPI center
            module
        '''
        status  = urllib.urlencode({'from': conf.IP[conf.MODE]})
        conn = httplib.HTTPConnection(to_ip, port=5000);
        conn.request("POST", "/test", status)
        content = conn.getresponse()
        print(content.reason, content.status)
        print(content.read())
        conn.close()
    except:
        print("It looks like " + to_ip + " isn't online!")
