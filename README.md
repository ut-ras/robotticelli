# Project Summary
 stuff.
 
# Building
 1. Get the XBeeLib
 2. Put it in a directory named `XBeeLib`
 3. Run `make` or `make all` or `make sender` or `make receiver`
 4. Install the UDEV rule, `52-user-frdm.rules` into udev (`sudo cp 52-user-frdm.rules /etc/udev/rules.d/`)
 4. ???
 5. Profit

# Flashing
  1. Go back and build a firmware
  2. Look in the `bin` directory for your firmware. It will be called one of :
    `bin/frdm-magi-sender.bin`, or
    `bin/frdm-magi-receiver.bin`
  3. List the availible boards with `./flash-boards.py -l`
  4. Pick a serial number from the list, and mark it for automatic update with 
    `./flash-boards.py -m <last-n-nibbles-of-the-serial> <firmware-filename-from-step-2>`
  5. Mark a few more boards
  6. All marked boards are automatically flashed with their correct firmware when you run `make flash-all`.
     If you only want to update one firmware, then run something like `make flash-receiver`
