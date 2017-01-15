import httplib

## Motor functions for communicating with the master RPi.
## Filled with functions to wrap HTTP request code.

def send_ready(from_ip, to_ip):
    '''
        This will let the main RPi module know
        that it is ready for the next motor
        instruction.
    '''
    status  = urllib.urlencode({'from': from_ip, 'status': 'ready'})

    conn = httplib.HTTPConnection(to_ip, port=5000);
    conn.request("POST", "/status", status)
    resp = conn.getresponse()
    print(content.reason, content.status)
    print(content.read())
    conn.close()
