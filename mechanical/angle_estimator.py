
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

_DX, _DY = .1, .1


def phi(x, y, plane=(50, 50), r1=(-.5, .5), r2=(.5, .5)):
    w, h = plane
    th1 = np.arctan2(h - y, x)
    th2 = np.arctan2(h - y, w - x)

    phi = np.arctan2(
        r1[0] * np.sin(th1) * np.cos(th2)
        + r1[1] * np.cos(th1) * np.cos(th2)
        + r2[0] * np.sin(th2) * np.cos(th1)
        - r2[1] * np.cos(th2) * np.cos(th1),

        r1[1] * np.sin(th1) * np.cos(th2)
        - r1[0] * np.cos(th1) * np.cos(th2)
        + r2[1] * np.sin(th2) * np.cos(th1)
        + r2[0] * np.cos(th2) * np.cos(th1)
    )

    return phi


def main():
    plane = (15, 15)
    shape = (plane[0] / _DX, plane[1] / _DY)
    r1, r2 = (-0.5, 0.5), (0.5, 0.5)
    result = np.fromiter((phi(i, j, plane=plane, r1=r1, r2=r2)
                          for i in np.arange(0, plane[0], _DX)
                          for j in np.arange(0, plane[1], _DY)),
                         np.float).reshape(shape)
    result = result.reshape(shape)

    hf = plt.figure()
    ha = hf.add_subplot(111, projection='3d')
    X, Y = np.meshgrid(np.arange(0, plane[1], _DY),
                       np.arange(0, plane[0], _DX))

    ha.plot_surface(X, Y, result)

    ha.set_xlabel("X")
    ha.set_ylabel("Y")
    plt.show()


if __name__ == '__main__':
    main()
