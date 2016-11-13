import numpy as np
from sklearn.cluster import MiniBatchKMeans

def median_cut(image, palette_size, color_database, deposit_c, overshoot, iternum = 0):
    # Hacky way of getting iterations from power
    iterations = palette_size.bit_length() + overshoot

    # Finds ranges for RGB
    ranges = np.max(a = image, axis = 0) - np.min(a = image, axis = 0)

    # Finds biggest range among all RGB color axes
    biggest_range = np.argmax(ranges)

    # Finds median values of the array, will pick the one along the
    # Axis with the highest range
    median = np.median(a = image, axis = 0)[biggest_range]

    # Access all R's, G's, or B's instead of a single RGB values
    image = np.transpose(image)

    # Finds colors whose indexes are bigger than or equal to median
    bgr_vals = np.where(image[biggest_range] >= median)[0]
    smr_vals = np.where(image[biggest_range] <  median)[0]

    # Put it back to its original shape
    image = np.transpose(image)

    # Adds the final iteration of the palette selection to a table
    if iternum == iterations - 1:
        if bgr_vals.size > 0:
            big_best   = [convert_to_database_palette([np.mean(image[bgr_vals],axis = 0)], color_database)]
            deposit_c.append(big_best[0][0][0])

        if smr_vals.size > 0:
            small_best = [convert_to_database_palette([np.mean(image[smr_vals],axis = 0)], color_database)]
            deposit_c.append(small_best[0][0][0])

    # Recurse if the function hasn't iterated enough times

    if iternum < iterations:
        iternum += 1
        if smr_vals.size > 0:
            median_cut(image[smr_vals], palette_size, color_database, deposit_c, overshoot, iternum)
        if bgr_vals.size > 0:
            median_cut(image[bgr_vals], palette_size, color_database, deposit_c, overshoot, iternum)
