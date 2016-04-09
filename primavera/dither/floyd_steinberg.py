 
import numpy as np
import scipy.spatial


def dither(image, reduced_image, palette):

    assert(image.shape == reduced_image.shape)

    # TODO: use better dithering algorithm
    # Options: ordered dithering
    print(palette)
    dithered = np.pad(np.array(image),
                      ((1, 1), (1, 1), (0, 0)),
                      mode='constant').astype(int)

    for x in range(1, image.shape[0] + 1):
        for y in range(1, image.shape[1] + 1):
            
            oldColor = np.copy(dithered[x][y])
            dithered[x][y] = palette[np.argmin(
                scipy.spatial.distance.cdist(
                    [dithered[x][y]], palette), axis=1)]

            error = oldColor - np.copy(dithered[x][y]) 
            #dithered[x][y] = error
            # NOTE: supposed to be 16, but we found 14 did better
            preSet10 = dithered[x + 0][y + 1] + [int(i) for i in error * 7./14]
            preSetN1 = dithered[x + 1][y - 1] + [int(i) for i in error * 3./14]
            preSet01 = dithered[x + 1][y + 0] + [int(i) for i in error * 5./14]
            preSet11 = dithered[x + 1][y + 1] + [int(i) for i in error * 1./14]

            preSet01[preSet01 > 255] = 255
            preSetN1[preSetN1 > 255] = 255
            preSet10[preSet10 > 255] = 255
            preSet11[preSet11 > 255] = 255

            preSet01[preSet01 < 0] = 0
            preSetN1[preSetN1 < 0] = 0
            preSet10[preSet10 < 0] = 0
            preSet11[preSet11 < 0] = 0

            dithered[x + 0][y + 1] = preSet01
            dithered[x + 1][y - 1] = preSetN1
            dithered[x + 1][y + 0] = preSet10
            dithered[x + 1][y + 1] = preSet11

    return dithered[1:-1, 1:-1, :]
