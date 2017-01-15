import numpy as np

def main():
    img_commands = np.genfromtxt('hardware/robot/image.tsv', delimiter='\t')
    print(img_commands)
