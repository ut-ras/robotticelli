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


def process_image(img, db,
                  palette_size=5,
                  scale=1.0,
                  dither='no_dither'):

    if dither:
        dither = importlib.import_module(
            'dither.%s' % (dither or 'no_dither')).dither

    names = np.array(list(db.keys()))
    colors = np.array([list(reversed(val)) for val in db.values()])
    palette, labels, image = detect_colors(img, args.palette_size, colors)

    image = dither(img, image, colors[palette])
    # image = downsample(image, args.scale)

    return image, labels, colors[palette]


def main():
    parser = argparse.ArgumentParser('primavera')
    parser.add_argument('-w', '--save-image', type=str)
    parser.add_argument('-l', '--save-labels', type=str)
    parser.add_argument('-p', '--palette-size', type=int, default=5)
    parser.add_argument('-c', '--colors', type=str, required=True)
    parser.add_argument('-d', '--dither', type=str, default='no_dither')
    parser.add_argument('-s', '--scale', type=float, default=1.0)
    parser.add_argument('--downsample-method', type=str)
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
