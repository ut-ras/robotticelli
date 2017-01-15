import numpy as np

def merge(color_set, final_value, image = False):
    """Takes a color_set input and merges colors until the
    color_set is of a desired size final_value. If image
    is passed, the merge algorithm will account for
    relative abundance of colors in the image when deciding
    how to merge colors"""

    # If an image is passed into the image argument, quick-sort will
    # be disabled, and the merge algorithm will factor in the prevalence
    # of colors when deciding what and how to merge.
    quickSortDisabled = (type(image) != bool)

    # The number of colors in our palette
    numberColors = color_set.shape[0]

    # If we have reached the right amounf of colors
    if numberColors <= final_value:
        return color_set

    # Calculates RGB distances between each color, determining
    # how different they are
    dists = np.round(cdist(color_set, color_set))

    # Will be used if
    prevalence = np.ones(numberColors)

    if quickSortDisabled:
        # Put image in terms of our current color set
        new_image, new_image_indexes = convert_to_database_palette(image, color_set)

        # Creating an array to dump relative prevalence of colors into.
        prevalence = np.zeros(numberColors)

        for i in range(numberColors):
            # Returns the number of positions in which the color is the
            # color being looked for in the loop
            prevalence[i] = 3*np.sum([new_image_indexes == i])/float(image.size)


        # Prevalence of each combo
        cross_prevalence = np.multiply.outer(prevalence, prevalence)

        # Recalculate distances factoring in color prevelance
        dists = np.multiply(dists, cross_prevalence)

    # The algorithm does not use vectorized operations
    # from here out and is NOT scalable.

    # Replaces axes with non-zero so that
    # they won't interfere with argmin
    for i in range(numberColors):
        dists[i][i] = 1000

    # Finds minimum x value
    foundX = np.argmin(np.min(dists, axis = 0))

    # We do this to search in only the upper triangle of the array
    # because our array is symetric and will give two of the same
    # values back otherwise
    foundY = np.argmin(np.min(dists, axis = 1)[foundX + 1:]) + (foundX + 1)


    # Coordinates in our dist array of the smallest value
    minimum = (foundX, foundY)

    # Value of the minimum
    minname =  np.min(dists, axis = (0, 1))

    newColorSet = np.array([])
    for index, color in enumerate(color_set):
        if index != foundX and index != foundY:
            newColorSet = np.append(newColorSet, color)
        elif index == foundX:
            pX = prevalence[foundX]
            pY = prevalence[foundY]

            midValue = (pX * color_set[foundX] + pY * color_set[foundY])/(pX + pY)
            newColorSet = np.append(newColorSet, midValue)

    newColorSet = newColorSet.reshape(newColorSet.size/3, 3)

    return merge(newColorSet, final_value, image)
