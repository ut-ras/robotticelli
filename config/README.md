
## Configuration

### RPi configuration

In order to connect to the RPi over the ethernet cable, you either have to set
both the rpi and the host machine to a static address, or set the RPi to request
for a dynamic address and the host machine to serve it.  It's simpler to do it
statically, and that's what the provided configuration does.

#### Sharing internet

In order to allow the RPi to access the internet through the host machine's WiFi
connection, run the `inet-share.sh` script.  It will install iproute rules to
forward the WiFi connection.
