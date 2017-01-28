from __future__ import absolute_import
from time import sleep
import numpy as np

import conf
from hardware.robot.motor_math import get_motor_spin_ratio
from hardware.robot.com import send_turn_ratio

##
## This is the code that instructs how to get from A to B
## using continual approximation and gradient descent
##

## Motors that have requested to move to the next step
## Only executes when all are true
## Motors have been assigned IDs which will then be
## Used to index motors_requested

## instructions has the following format per line:
## [CAN_NUMBER, X, Y]
instructions = np.genfromtxt('hardware/robot/image.tsv', delimiter='\t')
motors_requested = [True]

last_instruction_index = -1
current_instruction_index = 1
last_instruction = [1, -1, -1]
current_instruction = [1, -1, -1]

def check_all_requested():
    ## Returns true if all motors_requested values are true
    return reduce(lambda x, y: x and y, motors_requested)

## TODO: Integrate sensor data to complete this function
def position_is_close_enough_to_goal():
    return True

def gen_next_instruction():
    global current_instruction_index
    global current_instruction
    global last_instruction_index
    global last_instruction

    last_instruction, last_instruction_index = current_instruction, current_instruction_index
    current_instruction_index = current_instruction_index + 1
    current_instruction = instructions[current_instruction_index]

    while current_instruction[1] == -1:
        current_instruction_index = current_instruction_index + 1
        current_instruction = instructions[current_instruction_index]

    return current_instruction, current_instruction_index, last_instruction, last_instruction_index
##TODO: CHECK FOR LABEL CHANGES

def request_step(motor_id):
    global current_instruction_index
    global current_instruction
    global last_instruction_index
    global last_instruction

    print(motor_id)
    if motor_id < len(motors_requested):
        motors_requested[motor_id] = True

    if check_all_requested() and position_is_close_enough_to_goal():
        print("pass" + str(current_instruction_index))
        gen_next_instruction()
        print("pass")

        from_x, from_y = last_instruction[1], last_instruction[2]
        goal_x, goal_y = current_instruction[1], current_instruction[2]
        turn_ratio = get_motor_spin_ratio(
            from_x,
            from_y,
            (goal_x - from_x, goal_y - from_y)
        )
        ## We dont care about the direction of the other motor,
        ## Just the magnitude of how much it spins.
        ## So we need to take it's absolute value to get usable info
        ## This process is similar to atan2 in some ways

        ## Notice the array indices here are based on motor numerical
        ## IDs. 0 = top left, 1 = top right
        left_ratio = turn_ratio[0]/abs(turn_ratio[1])
        right_ratio = turn_ratio[1]/abs(turn_ratio[0])
        if conf.LMOTOR_IP != '0.0.0.0':
            send_turn_ratio(conf.LMOTOR_IP, left_ratio)
        if conf.RMOTOR_IP != '0.0.0.0':
            send_turn_ratio(conf.RMOTOR_IP, right_ratio)
