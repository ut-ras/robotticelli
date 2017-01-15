import conf

if conf.MODE == None:
    raise ValueError('Check conf.py to configure settings')

if conf.MODE == "PRE":
    from software.server import *
    print("Please visit 127.0.0.1:5000 to process image")
    app.run(port=5000,host='0.0.0.0')
