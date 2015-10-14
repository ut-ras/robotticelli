
import argparse
import cv2


def detect_colors(img, size):
    ret, _, center = cv2.kmeans(
        img.reshape((img.shape[0] * img.shape[1], 3)).astype('float32'),
        size, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
        10, cv2.KMEANS_RANDOM_CENTERS)

    # LOG.info("Compactness: {}".format(ret))

    return ((int(r), int(g), int(b)) for (b, g, r) in center)


def select_palette(colors):
    db = [
        (0, 255, 255), # Cyan
        (255, 0, 255), # Magenta
        (255, 255, 0), # Yellow
        (0, 0, 0) # Black
        ]
    print([color for color in colors])


def main():
    parser = argparse.ArgumentParser('primavera')
    parser.add_argument('--image')
    parser.add_argument('-p', '--palette-size', type=int)

    args = parser.parse_args()

    img = cv2.imread(args.image)
    if img is None:
        raise ValueError("Invalid image file/format")

    select_palette(detect_colors(img, args.palette_size))


if __name__ == '__main__':
    main()
