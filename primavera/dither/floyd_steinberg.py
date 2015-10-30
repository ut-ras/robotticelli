
import numpy as np
import scipy.spatial


def dither(image, reduced_image, palette):
    assert(image.shape == reduced_image.shape)

    # TODO: use better dithering algorithm
    # Options: ordered dithering

    dithered = np.pad(np.array(reduced_image),
                      ((1, 1), (1, 1), (0, 0)),
                      mode='constant')

    for x in range(1, image.shape[0] + 1):
        for y in range(1, image.shape[1] + 1):
            dithered[x][y] = palette[np.argmin(
                scipy.spatial.distance.cdist(
                    [dithered[x][y]], palette), axis=1)]
            error = image[x - 1][y - 1] - dithered[x][y]
            # NOTE: supposed to be 16, but we found 14 did better
            dithered[x + 1][y + 0] += [int(i) for i in error * 7./14]
            dithered[x - 1][y + 1] += [int(i) for i in error * 3./14]
            dithered[x + 0][y + 1] += [int(i) for i in error * 5./14]
            dithered[x + 1][y + 1] += [int(i) for i in error * 1./14]

    return dithered[1:-1, 1:-1, :]
