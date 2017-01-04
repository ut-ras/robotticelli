import numpy as np

def checkInconsistent(image):
    '''Debugging tool to check that the colors picked for the image
    match the colors in the output'''

    print("scanning image for final colors")
    print("check for inconsistencies...")

    h, w  = image.shape[:2]
    image = image.reshape(h * w, 3)
    uniqueColors = np.unique(tuple(color) for color in image)

    print(("final colors in image: " + str(uniqueColors)))
