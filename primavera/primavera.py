import argparse
import importlib
import math
import json

import cv2
import numpy as np
import scipy as sp
from sklearn.cluster import MiniBatchKMeans


def convert_to_database_palette(image, color_database):
    """ A collection of indexes to the colors in our database that best
    represents its respective pixel sp.spatial.distance.cdist finds the
    distance between the colors in our database and each pixel in our image
    np.argmin finds the index of the smallest distance (aka the closest color)
    """
    database_indexes = np.argmin(sp.spatial.distance.cdist(
        image, color_database), axis=1)

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

def detect_colors(image, palette_size, color_database):
    """ find the best set of colors for an image given a color database and a pallete size
    """

    # Takes all the colors in the image and puts them side-by-side so that
    # they can be iterated through more easily
    h, w  = image.shape[:2]
    image = image.reshape(h * w, 3)

    # Gives us a rouge palette for this image
    centers = cluster_colors_into_groups(image, palette_size)

    # Approximates this palette in terms of spray paint colors
    new_palette, palette_indexes = convert_to_database_palette(
        centers[0], color_database)

    # Puts the image in terms of the spray paint palette we just found
    new_image, new_image_indexes = convert_to_database_palette(
        image, new_palette)

    return (palette_indexes,
            new_image_indexes.reshape((h, w)),
            new_image.reshape((h ,w , 3)))


def process_image(img, db,
                  palette_size=5,
                  scale=1.0,
                  dither='no_dither'):

    if dither:
        dither = importlib.import_module(
            'dither.%s' % (dither or 'no_dither')).dither

    names, colors = [np.array(i) for i in zip(*db.iteritems())]
    palette, labels, image = detect_colors(img, palette_size, colors)

    image = dither(img, image, colors[palette])
    image = sp.misc.imresize(image, scale)

    return image, labels, names[palette]


def main():
    parser = argparse.ArgumentParser('primavera')
    parser.add_argument('-w', '--save-image', type=str)
    parser.add_argument('-l', '--save-labels', type=str)
    parser.add_argument('-p', '--palette-size', type=int, default=5)
    parser.add_argument('-c', '--colors', type=str, required=True)
    parser.add_argument('-d', '--dither', type=str, default='no_dither')
    parser.add_argument('-s', '--scale', type=float, default=1.0)
    parser.add_argument('IMAGE')

    args = parser.parse_args()

    img = cv2.imread(args.IMAGE)
    if img is None:
        raise ValueError("Invalid image file/format")

    db = json.load(open(args.colors))
    image, labels, colors = process_image(img, db,
                                          palette_size=args.palette_size,
                                          scale=args.scale,
                                          dither=args.dither)

    print('\n'.join(colors))

    if args.save_labels:
        np.save(args.save_labels, labels)

    if args.save_image:
        cv2.imwrite(args.save_image, image)

if __name__ == '__main__':
    main()
