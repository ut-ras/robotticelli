#! /usr/bin/env python
#
#

from pyOCD.board import MbedBoard

board = MbedBoard.chooseBoard();

target = board.target
flash = board.flash
target.resume()
target.halt()


print "pc: 0x%X" % target.readCoreRegister("pc")

target.step()
print "pc: 0x%X" % target.readCoreRegister("pc")

flash.flashBinary("frdm_test.bin")
print "pc: 0x%X" % target.readCoreRegister("pc")

target.reset()
target.halt()

print "pc: 0x%X" % target.readCoreRegister("pc")

board.uninit()
