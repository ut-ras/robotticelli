#! /usr/bin/env python2


from pyOCD.board import MbedBoard
import argparse
import json
import io
import os

def createWriteableFile (name) :
    return open(name, 'r+')

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description = "flash a board with sender or reciever code")
    parser.add_argument('firmware', type=str, nargs='*', metavar='FIRMWARE'
                        , help='flash FIRMWARE to marked BOARDS')
    parser.add_argument('-m', '--mark', type=str,  metavar='BOARD'
                        , help='mark BOARD to be flashed by only the FIRMWARE (fails if more than one FIRMWARE is provided)')
    parser.add_argument('-c', '--config', type=createWriteableFile
                        , metavar='CONFIG', help='CONFIG file to use'
                        , default='.board-config.json')
    parser.add_argument('-l', '--list', action='store_true'
                        , help='list all connected boards')
    parser.add_argument
    args = parser.parse_args()
    if args.list :
        for board in MbedBoard.getAllConnectedBoards() :
            print("{} ID: {}".format(board.getTargetType(),board.getUniqueID()))
        exit(0)

    if args.mark is not None and len(args.firmware) != 1:
        print("ERROR: you must provide exactly one FIRMWARE when marking a BOARD")
        exit(1)

    try:
        config = json.load(args.config)
    except ValueError:
        print("WARNING: configuration file corrupted")
        config = {}

    for board in MbedBoard.getAllConnectedBoards() :
        if args.mark is not None \
           and board.getUniqueID().upper().endswith(args.mark.upper()) :
            config[board.getUniqueID()] = args.firmware[0]
        if board.getUniqueID() in config \
           and config[board.getUniqueID()] in args.firmware :
            print("Flashing board {} with {}".format(board.getUniqueID()
                                                     , config[board.getUniqueID()]))
            board.init()
            target = board.target
            flash = board.flash
            target.resume()
            target.halt()
            target.step()
            flash.flashBinary(config[board.getUniqueID()])
            target.reset()
            target.halt()
            board.uninit()

    args.config.seek(0)
    json.dump(config,args.config,indent=4)
    args.config.close()
