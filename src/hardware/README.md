#Magi

Contains all the code that drives robotticelli's hardware.
Since we are currently using Raspberry Pi 3 Model Bs as all
of our devices, this code is written in python.

'robot' contains all code relevant to the raspberry pi running
on the robot's frame, whereas 'motor' contains all of the
relevant code for the winch mechanisms carrying the robot around.

All devices will be connected to a private WiFi network and
communicating to eachother through a webserver on each device.
Devices will be addressed via private IPs.

----

Both 'motor' and 'robot' have three pieces of code that execute:

*main.py* is how src.main bootstraps all the code in the executed directory,
as well as spawns any benificial background processes

*server.py* is used to listen for partners over the :5000 port.

*run.py* is collection of functions that is forked to a
background worker and executed concurrently with *server.py*.

Code is also broken out into other scripts that are imported to
main, server, and run. These scripts are located in the
*(motor|robot)/modules* directory.
