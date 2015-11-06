USER_LIB_PATH = ../../lib/arduino
BOARD_TAG    = mega
BOARD_SUB    = atmega2560

ARDUINO_LIBS = xbee-arduino
SCREEN := screen

include /usr/share/arduino/Arduino.mk
uart:
	$(SCREEN) /dev/ttyACM0 115200
