import numpy as np
from hardware.robot.motor_math import get_motor_spin_ratio

## NOTE: This module is going to be deleted soon in favor
## of merging it with a function of server.py
## Keeping it here to extract the code later

def main():
    img_commands = np.genfromtxt('hardware/robot/image.tsv', delimiter='\t')
    from_x, from_y = 0, 0
    for number, cell in enumerate(img_commands):
        ## Doing this because I signify color switches by
        ## putting -1 as a coordinate
        if cell[1] != -1:
            x, y = cell[1], cell[2]
            dir_x, dir_y = (x)
            turn_ratio = get_motor_spin_ratio(
                from_x,
                from_y,
                (x - from_x, y - from_y)
            )
