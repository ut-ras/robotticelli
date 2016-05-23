import argparse
import importlib
import math
import json

import cv2
import numpy as np
import scipy as sp
from scipy.spatial.distance import cdist
from sklearn.cluster import MiniBatchKMeans


def convert_to_database_palette(image, color_database):
    """ A collection of indexes to the colors in our database that best
    represents its respective pixel sp.spatial.distance.cdist finds the
    distance between the colors in our database and each pixel in our image
    np.argmin finds the index of the smallest distance (aka the closest color)
    """

    # Print(color_database)
    database_indexes = np.argmin(cdist(image, color_database), axis=1)

    # Takes the indexes found in db_idx (color database indexes) and creates
    # an image out of it
    return color_database[database_indexes], database_indexes

def cluster_colors_into_groups(image, clusters):
    # Performs k-means clustering on the colors in the image
    clt = MiniBatchKMeans(n_clusters=clusters)
    clt.fit_predict(image)

    # Returns the centers of the found clusters
    # These centers will give the color that the cluster is representing
    # as coordinates in RGB space
    return np.array([clt.cluster_centers_.astype("uint8")])

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

def median_cut(image, palette_size, color_database, deposit_c, overshoot, iternum = 0):
    # Hacky way of getting iterations from power
    iterations = np.ceil(np.log(palette_size)/np.log(2)) + overshoot

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
            median_cut(image[smr_vals], palette_size, color_database, deposit_c, iternum)
        if bgr_vals.size > 0:
            median_cut(image[bgr_vals], palette_size, color_database, deposit_c, iternum)




def detect_colors(image, palette_size, color_database, quick = False, entire = False, overshoot = 1, doNotMerge = False):
    """ find the best set of colors for an image given a color database and a pallete size
    """

    # Takes all the colors in the image and puts them side-by-side so that
    # they can be iterated through more easily
    h, w  = image.shape[:2]
    image = image.reshape(h * w, 3)

    # the array that median cut will return its results into
    best_colors  = []
    best_indices = []

    # picks colors
    if not entire:
        median_cut(image, palette_size, color_database, best_colors, overshoot)

    # gets rid of color repeats
    uniqueColors = np.unique(tuple(color) for color in best_colors)

    # merges similar colors to reduce palette to palette_size

    reduced_colors = color_database

    if not doNotMerge or not entire:
        reduced_colors = merge(uniqueColors, palette_size, image = (False if quick else image))

    # finds best palette
    new_palette, palette_indexes = convert_to_database_palette(color_database if entire else reduced_colors, color_database)

    # Puts the image in terms of the spray paint palette we just found
    new_image, new_image_indexes = convert_to_database_palette(image, new_palette)

    return (palette_indexes,
            new_image_indexes.reshape((h, w)),
            new_image.reshape((h ,w , 3)))

def checkInconsistent(image):
    print("scanning image for final colors")
    print("check for inconsistencies...")

    h, w  = image.shape[:2]
    image = image.reshape(h * w, 3)
    uniqueColors = np.unique(tuple(color) for color in image)

    print("final colors in image: " + str(uniqueColors))

def main():
    parser = argparse.ArgumentParser('primavera')
    parser.add_argument('-i', '--image', required=True)
    parser.add_argument('-p', '--palette-size', type=int, default=5)
    parser.add_argument('-w', '--save-image', type=str)
    parser.add_argument('-s', '--save-labels', type=str)
    parser.add_argument('-c', '--colors', type=str, required=True)
    parser.add_argument('-d', '--dither', type=str)
    parser.add_argument('-r', '--resize', type=float, default=1)
    parser.add_argument('-o', '--overshoot', type=int, default=1)
    parser.add_argument('-m', '--merge',  action="store_true")
    parser.add_argument('-q', '--quick',  action="store_true")
    parser.add_argument('-e', '--entire', action="store_true")

    args = parser.parse_args()
    img  = cv2.imread(args.image)

    if img is None:
        raise ValueError("Invalid image file/format")

    if args.resize != 1:
        img = sp.misc.imresize(img, args.resize)

    database = json.load(open(args.colors))
    names    = np.array(list(database.keys()))
    colors   = np.array([list(reversed(val)) for val in database.values()])

    palette, labels, image = detect_colors(img, args.palette_size, colors, args.quick, args.entire, args.overshoot, args.merge)

    if args.dither:
        dither = importlib.import_module('dither.%s' % args.dither).dither
        image  = dither(img, image, colors[palette])

    checkInconsistent(image)

    if args.save_labels:
        np.save(args.save_labels, labels)

    if args.save_image:
        cv2.imwrite(args.save_image, image)

    print('\n'.join(names[palette]))

if __name__ == '__main__':
    main()
