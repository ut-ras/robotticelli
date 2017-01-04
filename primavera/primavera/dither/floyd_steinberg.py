
import numpy as np
import scipy.spatial

def dither(image, palette):
    dithered = np.pad(np.array(image),
                      ((1, 1), (1, 1), (0, 0)),
                      mode='constant').astype(int)

    palette_kdtree = scipy.spatial.KDTree(palette)

    for x in range(1, image.shape[0] + 1):
        for y in range(1, image.shape[1] + 1):

            oldColor = np.copy(dithered[x][y])
            dithered[x][y] = palette[palette_kdtree.query(dithered[x][y], 1)[1]]

            error = np.array(oldColor - dithered[x][y]).astype(int)
            #dithered[x][y] = error
            preSet10 = dithered[x + 0][y + 1] + error * 7./16
            preSetN1 = dithered[x + 1][y - 1] + error * 3./16
            preSet01 = dithered[x + 1][y + 0] + error * 5./16
            preSet11 = dithered[x + 1][y + 1] + error * 1./16

            dithered[x + 0][y + 1] = np.clip(preSet01, 0, 255)
            dithered[x + 1][y - 1] = np.clip(preSetN1, 0, 255)
            dithered[x + 1][y + 0] = np.clip(preSet10, 0, 255)
            dithered[x + 1][y + 1] = np.clip(preSet11, 0, 255)

    return dithered[1:-1, 1:-1, :]
