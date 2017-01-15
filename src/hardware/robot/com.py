import httplib
import urllib

def send_turn_ratio(from_ip, to_ip, ratio):
    '''
        This will let the main RPi module know
        that it is ready for the next motor
        instruction.
    '''
    status  = urllib.urlencode({'from': from_ip, 'turn_ratio': ratio})
    conn = httplib.HTTPConnection(to_ip, port=5000);
    conn.request("POST", "/", status)
    resp = conn.getresponse()
    print(content.reason, content.status)
    print(content.read())
    conn.close()
