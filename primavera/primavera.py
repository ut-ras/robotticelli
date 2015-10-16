
import argparse
import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans


def detect_colors(image, size, as_lab=False):
    h, w = image.shape[:2]
    if as_lab:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    image = image.reshape((h * w, 3))
    # TODO: remove transparency before running KMeans

    clt = MiniBatchKMeans(n_clusters=size)
    # TODO: Fit without alpha, predict with alpha
    labels = clt.fit_predict(image).reshape((h, w))
    centers = np.array([clt.cluster_centers_.astype("uint8")])
    if as_lab:
        centers = cv2.cvtColor(centers, cv2.COLOR_LAB2BGR)
    image = clt.cluster_centers_.astype("uint8")[labels]

    image = image.reshape((h, w, 3))
    if as_lab:
        image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)

    return [(int(r), int(g), int(b)) for (b, g, r) in centers[0]], labels, image


def select_palette(colors):
    return colors


def main():
    parser = argparse.ArgumentParser('primavera')
    parser.add_argument('--image')
    parser.add_argument('-p', '--palette-size', type=int)
    parser.add_argument('-w', '--save-image', type=str)
    parser.add_argument('-s', '--save-labels', type=str)

    args = parser.parse_args()

    img = cv2.imread(args.image)
    if img is None:
        raise ValueError("Invalid image file/format")

    colors, labels, image = detect_colors(img, args.palette_size)
    # Dither

    print(colors)

    if args.save_labels:
        np.save(args.save_labels, labels)

    if args.save_image:
       cv2.imwrite(args.save_image, image)


if __name__ == '__main__':
    main()
