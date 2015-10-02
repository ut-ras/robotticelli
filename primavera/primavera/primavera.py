
import argparse
import cv2


def select_palette(img, size):
    ret, _, center = cv2.kmeans(
        img.reshape((img.shape[0] * img.shape[1], 3)).astype('float32'),
        size, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
        10, cv2.KMEANS_RANDOM_CENTERS)

    # LOG.info("Compactness: {}".format(ret))

    return center


def main():
    parser = argparse.ArgumentParser('primavera')
    parser.add_argument('--image')
    parser.add_argument('-p', '--palette-size', type=int)

    args = parser.parse_args()

    img = cv2.imread(args.image)
    if img is None:
        raise ValueError("Invalid image file/format")

    print(select_palette(img, args.palette_size))


if __name__ == '__main__':
    main()
