import numpy as np

from .quantize import *
from .merge import merge

def detect_colors(image, palette_size, color_database, quick = False,
                  entire = False, overshoot = 1, doNotMerge = False):
    """ find the best set of colors for an image given a color database
    and a pallete size"""

    # Takes all the colors in the image and puts them side-by-side so that
    # they can be iterated through more easily
    h, w  = image.shape[:2]
    image = image.reshape(h * w, 3)

    ## Uses median cut to find the best colors
    best_colors = median_cut(image, palette_size, color_database, overshoot)

    unique_colors = np.array(best_colors)
    #np.unique([tuple(color) for color in best_colors])
    # merges similar colors to reduce palette to palette_size

    reduced_colors = unique_colors

    if not doNotMerge and not entire:
        reduced_colors = merge(unique_colors, palette_size,
                               image = (False if quick else image))

    if entire:
        reduced_colors = color_database

    # finds best palette
    new_palette, palette_indexes = convert_to_database_palette(reduced_colors, color_database)

    # Puts the image in terms of the spray paint palette we just found
    new_image, new_image_indexes = convert_to_database_palette(image, new_palette)
   
    for index, pixel in enumerate(new_image):
        if tuple(pixel) == (255, 255, 255):
            new_image_indexes[index] = -1

    return (palette_indexes,
            new_image_indexes.reshape((h, w)),
            new_image.reshape((h ,w , 3)))
