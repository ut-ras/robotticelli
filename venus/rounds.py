# In this step, we need to divide the image into disjoint sets. Each set
# must satisfy the following properites:
#       - contain at most N colors, where N is the number of cans
#       - for each color, have at most (max pixels per can) pixels
# The ideal solution will form a set that maximizes the number of pixels
# sprayed and minimize distance between pixels. It's important to create
# a set of adjacent pixels rather than a sparse array.

# Inputs:
#       - pixels                numpy.ndarray of Integers
#       - max pixels per can    Integer
#       - number of cans        Integer
# Outputs:
#       - set(([(x, y, can number)], [(color, can number)]))

import argparse

def main():
    pass

if __name__ == '__main__':
    main()
