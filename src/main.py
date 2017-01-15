import conf

def robotticelli():
    if conf.MODE == None:
        raise ValueError('Check conf.py to configure settings')

    if conf.MODE == "PRE":
        import software.server
        app.run(port=5000,host='0.0.0.0')

if __name__ == "main":
    robotticelli()
