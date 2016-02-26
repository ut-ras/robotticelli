#!/usr/bin/env python2
from pyOCD.board import MbedBoard

board = MbedBoard.chooseBoard()

target = board.target
flash = board.flash
target.resume()
target.halt()

flash.flashBinary("frdm_test.bin")

target.reset()
target.halt()

board.uninit()
