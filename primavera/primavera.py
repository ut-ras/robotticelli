
import argparse
import cv2
import json
import numpy as np
import scipy.spatial
from sklearn.cluster import MiniBatchKMeans


def detect_colors(image, size, database, as_lab=False):
    if as_lab:
        raise ValueError("Cannot support LAB")

    h, w = image.shape[:2]

    if as_lab:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    image = image.reshape((h * w, 3))
    # Indexes to the database that best represents the image
    db_idx = np.argmin(scipy.spatial.distance.cdist(image, database), axis=1)
    # Convert the image as best as possible to our database
    image = database[db_idx]
    # TODO: remove transparency before running KMeans

    clt = MiniBatchKMeans(n_clusters=size)
    # TODO: Fit without alpha, predict with alpha
    labels = clt.fit_predict(image)
    centers = np.array([clt.cluster_centers_.astype("uint8")])
    if as_lab:
        centers = cv2.cvtColor(centers, cv2.COLOR_LAB2BGR)

    # Find the colors in our database that best match each label
    bins, _, _ = np.histogram2d(
        labels, db_idx, bins=[len(centers[0]), len(database)])
    centers_to_db = np.argmax(bins, axis=1)

    # Convert the output image to our database
    image_in_db_idx = centers_to_db[labels]
    image = database[image_in_db_idx]

    image = image.reshape((h, w, 3))
    if as_lab:
        image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)

    return np.unique(centers_to_db), image_in_db_idx.reshape((h, w)), image


def select_palette(colors):
    return colors


def main():
    parser = argparse.ArgumentParser('primavera')
    parser.add_argument('--image')
    parser.add_argument('-p', '--palette-size', type=int)
    parser.add_argument('-w', '--save-image', type=str)
    parser.add_argument('-s', '--save-labels', type=str)
    parser.add_argument('-d', '--database', type=str, required=True)

    args = parser.parse_args()

    img = cv2.imread(args.image)
    if img is None:
        raise ValueError("Invalid image file/format")

    db = np.array(json.load(open(args.database)))
    colors, labels, image = detect_colors(img, args.palette_size, db)
    # Dither

    print(colors)

    if args.save_labels:
        np.save(args.save_labels, labels)

    if args.save_image:
        cv2.imwrite(args.save_image, image)


if __name__ == '__main__':
    main()
