import conf

if conf.MODE == None:
    raise ValueError('Check conf.py to configure settings')

elif conf.MODE == "SETUP":
    from software.server import *
    print("Please use a browser visit 127.0.0.1:5000 to process image")
    app.run(port=5000,host='0.0.0.0')

elif conf.MODE == "ROBOT":
    from hardware.robot.main import main
    main()

else:
    raise ValueError('Please check conf mode for typos')
