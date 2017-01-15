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
