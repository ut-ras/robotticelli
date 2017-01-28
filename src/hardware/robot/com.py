import httplib
import urllib
import conf

##Module for communicating to the slaves.
##Wraps long HTTPRequests

def send_turn_ratio(to_ip, ratio):
    '''
        This will let the main RPi module know
        that it is ready for the next motor
        instruction.
    '''
    status  = urllib.urlencode({'from': conf.IP[conf.MODE], 'turn_ratio': ratio})
    conn = httplib.HTTPConnection(to_ip, port=5000);
    conn.request("POST", "/", status)
    resp = conn.getresponse()
    print(content.reason, content.status)
    print(content.read())
    conn.close()

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
