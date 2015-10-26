
import argparse
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


_DX = .05
_DY = .05
_g = 9.81


def _solve_at_point(B, Term, P, R):
    # NOTE: Specific to the tension of the cable
    Fmag = Term - R - P[:4]

    F = np.vstack((
        Fmag / np.linalg.norm(Fmag, axis=1)[:, np.newaxis],
        np.array([[0, 0, 1], [0, 0, 1]])
    ))

    A = np.vstack((
        F.T,
        np.cross(P, F).T
    ))

    try:
        if (abs(R[0] - 1.55) < .00001 and
                abs(R[1] - 3.8) < .00001 and
                abs(R[2] - 0) < .00001):
            raise StopIteration("Found target point")

        return [np.linalg.det(A)]
        return np.linalg.solve(A, -B)
    except Exception as e:
        print("%s\nR = %s\n\n"
              "B =\n%s\n\n"
              "Term =\n%s\n\n"
              "P =\n%s\n\n"
              "F =\n%s\n\n"
              "F_norm =\n%s\n\n"
              "A =\n%s\n" %
              (e, R, B, Term, P, Fmag, F, A))
        if isinstance(e, StopIteration):
            return [np.linalg.det(A)]
            pass
            # exit(0)

        raise e
        return np.array([5e20, 5e20, 5e20,
                        5e20, 5e20, 5e20])


def solve_over_plane(plane=(33., 33.), robot=(.5, .5, .2), mass=10.):
    N3 = 5.
    Fg = _g * mass

    pw, ph = np.array(plane)
    rw, rh, _ = np.array(robot) / 2
    rd = robot[2]

    P = np.vstack((
        np.array([-rw,  rh, rd]),
        np.array([rw,   rh, rd]),
        np.array([-rw, -rh, rd]),
        np.array([rw,  -rh, rd]),
        np.array([-rw,  rh,  0]),
        np.array([rw,   rh,  0]),
    ))

    Term = np.vstack((
        np.array([0,  ph, 0]),
        np.array([pw, ph, 0]),
        np.array([0,  0,  0]),
        np.array([pw, 0,  0]),
    ))

    B = np.matmul(np.vstack((
        [0,  0],
        [-1, 0],
        [0,  1],
        [rd/2,  -rh],
        [0,  0],
        [0,  0],

    )), [Fg, N3])

    shape = (int((pw - 2*rw + _DX) / _DX),
             int((ph - 2*rh + _DY) / _DY),
             # 6)
             1)
    result = np.fromiter((k
                          for i in range(shape[0])
                          for j in range(shape[1])
                          # ),
                          for k in _solve_at_point(
                              B, Term, P,
                              np.array([(i * _DX) + rw, (j * _DY) + rh, 0]))),
                         np.float).reshape(shape)

    return result


def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('--plane', type=float, nargs=2, default=(5., 5.))
    parser.add_argument('--robot', type=float, nargs=3, default=(.5, .5, .2))
    parser.add_argument('--mass', type=float, default=10.)
    args = parser.parse_args()

    result = solve_over_plane(plane=args.plane,
                              robot=args.robot,
                              mass=args.mass)
    shape = result.shape

    hf = plt.figure()
    ha = hf.add_subplot(111, projection='3d')
    X, Y = np.meshgrid(range(shape[0]), range(shape[1]))

    # for force, color in zip(range(4),
    for force, color in zip(range(1),
                            ['blue', 'red', 'yellow',
                             'green', 'purple', 'orange']):
        ha.plot_surface(X[10:-10, 10:-10],
                        Y[10:-10, 10:-10],
                        result[10:-10, 10:-10, force], color=color)

    ha.set_xlabel("X")
    ha.set_ylabel("Y")
    plt.show()


if __name__ == '__main__':
    main()
