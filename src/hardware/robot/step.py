import numpy as np
from hardware.robot.motor_math import get_motor_spin_ratio

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
motors_requested = [False, False]
last_instruction = -1
current_instruction = 0

def check_all_requested():
    ## Returns true if all motors_requested values are true
    return reduce(lambda x, y: x and y, motors_requested)

## TODO: Integrate sensor data to complete this function
def position_is_close_enough_to_goal():
    return True

def gen_next_instruction():
    last_instruction    = current_instruction
    current_instruction = current_instruction + 1

    while current_instruction[1] == -1:
        current_instruction = current_instruction + 1

##TODO: CHECK FOR LABEL CHANGES

def request_step(motor_id):
    motors_requested[motor_id] = True
    if check_all_requested() and position_is_close_enough_to_goal():
        gen_next_instruction()
        from_x = last_instruction[1]
        from_y = last_instruction[2]
        goal_x = current_instruction[1]
        goal_y = current_instruction[2]
        turn_ratio = get_motor_spin_ratio(
            from_x,
            from_y,
            (goal_x - from_x, goal_y - from_y)
        )
