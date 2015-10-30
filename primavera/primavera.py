import argparse
import importlib
import math
import json

import cv2
import numpy as np
import scipy as sp
from sklearn.cluster import MiniBatchKMeans


def downsample(image):

    newX = image.shape[0]/2 - 1
    newY = image.shape[1]/2 - 1

    downsampled = np.zeros((newX, newY, 3))

    for x in range(0, newX):
        for y in range(0, newY):
            color1 = image[2*x + 0][2*y + 0]
            color2 = image[2*x + 0][2*y + 1]
            color3 = image[2*x + 1][2*y + 0]
            color4 = image[2*x + 1][2*y + 1]

            colors = [color1, color2, color3, color4]

            maxColor = [0, 0, 0]
            for i in range(0, 3):
                if np.linalg.norm(colors[i]-maxColor) > 0:
                    maxColor = colors[i]

            downsampled[x][y] = maxColor

    return downsampled[:, :, :]


def detect_colors(image, palette_size, database):
    h, w = image.shape[:2]

    image = image.reshape((h * w, 3))
    # Indexes to the database that best represents the image
    db_idx = np.argmin(sp.spatial.distance.cdist(image, database), axis=1)

    # Convert the image as best as possible to our database
    image = database[db_idx]
    # TODO: remove transparency before running KMeans

    clt = MiniBatchKMeans(n_clusters=palette_size)
    # TODO: Fit without alpha, predict with alpha
    labels = clt.fit_predict(image)
    centers = np.array([clt.cluster_centers_.astype("uint8")])

    bins = np.zeros((len(centers[0]), len(database)))
    for i, j in zip(labels, db_idx):
        bins[i][j] += 1
    centers_to_db = np.argmax(bins, axis=1)

    # Convert the output image to our database
    image_in_db_idx = centers_to_db[labels]
    reduced_image = database[image_in_db_idx].reshape((h, w, 3))

    palette = np.unique(centers_to_db)

    return (palette,
            image_in_db_idx.reshape((h, w)),
            reduced_image)


def main():
    parser = argparse.ArgumentParser('primavera')
    parser.add_argument('-i', '--image', required=True)
    parser.add_argument('-p', '--palette-size', type=int, default=5)
    parser.add_argument('-w', '--save-image', type=str)
    parser.add_argument('-s', '--save-labels', type=str)
    parser.add_argument('-c', '--colors', type=str, required=True)
    parser.add_argument('-d', '--dither', type=str)
    parser.add_argument('-m', '--down-sample', action='store_true')

    args = parser.parse_args()

    img = cv2.imread(args.image)
    # img = scipy.ndimage.imread(args.image)
    if img is None:
        raise ValueError("Invalid image file/format")

    db = json.load(open(args.colors))
    names = np.array(list(db.keys()))
    colors = np.array([list(reversed(val)) for val in db.values()])
    palette, labels, image = detect_colors(img, args.palette_size, colors)

    if args.dither:
        dither = importlib.import_module('dither.%s' % args.dither).dither
        image = dither(img, image, colors[palette])

    if args.down_sample:
        image = downsample(image)
    print('\n'.join(names[palette]))

    if args.save_labels:
        np.save(args.save_labels, labels)

    if args.save_image:
        # scipy.misc.imsave(args.save_image, image)
        cv2.imwrite(args.save_image, image)


if __name__ == '__main__':
    main()
