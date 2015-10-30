
import numpy as np
import scipy.spatial


def dither(image, reduced_image, palette):
    assert(image.shape == reduced_image.shape)

    thresholdMap = [
        [01./65, 49./65, 13./65, 61./65,  4./65, 52./65, 16./65, 64./65],
        [33./65, 17./65, 45./65, 29./65, 36./65, 20./65, 48./65, 32./65],
        [09./65, 57./65,  5./65, 53./65, 12./65, 60./65,  8./65, 56./65],
        [41./65, 25./65, 37./65, 21./65, 44./65, 28./65, 40./65, 24./65],
        [03./65, 51./65, 15./65, 63./65,  2./65, 50./65, 14./65, 62./65],
        [35./65, 19./65, 47./65, 31./65, 34./65, 18./65, 46./65, 30./65],
        [11./65, 59./65,  7./65, 55./65, 10./65, 58./65,  6./65, 54./65],
        [43./65, 27./65, 39./65, 23./65, 42./65, 26./65, 38./65, 22./65]
    ]

    dithered = np.array(image)

    for x in range(0, image.shape[0]):
        for y in range(0, image.shape[1]):

            thresholdValue = thresholdMap[x % 8][y % 8]

            old = np.array(dithered[x][y])
            if (old[0] != 255 and old[1] != 255 and old[2] != 255):
                old[0] *= (.5 + .5 * thresholdValue)
                old[1] *= (.5 + .5 * thresholdValue)
                old[2] *= (.5 + .5 * thresholdValue)

            best = [0, 0, 0]
            cost = float('inf')

            dithered[x][y] = palette[np.argmin(
                scipy.spatial.distance.cdist(
                    [old], palette), axis=1)]

    return dithered[:, :, :]
