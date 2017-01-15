import argparse
import importlib
import math
import json
import numpy as np
import scipy as sp

from .modules.colors import detect_colors

def primavera(image, colors, dither, palette_size=5, save_image='out.png', save_labels='lout.png',
              resize=1, overshoot=1, merge=True, quick=False, entire=False):

    img  = sp.misc.imread(image)

    if img is None:
        raise ValueError("Invalid image file/format")

    if resize != 1:
        img = sp.misc.imresize(img, resize)

    database = json.load(open(colors))
    names    = np.array(list(database.keys()))
    colors   = np.array([list(reversed(val)) for val in list(database.values())])

    palette, labels, image = detect_colors(img, palette_size, colors, quick, entire, overshoot, merge)

    if dither:
        if __name__ != "main":
            dither = importlib.import_module('%s.dither.%s' % (str(__name__)[:-10],dither)).dither
        else:
            dither = importlib.import_module('.dither.%s' % dither).dither

        image  = dither(img, colors[palette])

    #checkInconsistent(image)

    if save_labels:
        np.save(save_labels, labels)

    if save_image:
        sp.misc.insave(save_image, image)

    return labels

def main():
    parser = argparse.ArgumentParser('primavera')
    parser.add_argument('-i', '--image', required=True)
    parser.add_argument('-p', '--palette-size', type=int, default=5) #
    parser.add_argument('-w', '--save-image', type=str)
    parser.add_argument('-s', '--save-labels', type=str)
    parser.add_argument('-c', '--colors', type=str, required=True) #
    parser.add_argument('-d', '--dither', type=str) #
    parser.add_argument('-r', '--resize', type=float, default=1)
    parser.add_argument('-o', '--overshoot', type=int, default=1) #
    parser.add_argument('-m', '--merge',  action="store_true") #
    parser.add_argument('-q', '--quick',  action="store_true") #
    parser.add_argument('-e', '--entire', action="store_true")

    args = parser.parse_args()

    primavera(image=args.image, palette_size=args.palette_size, save_image=args.save_image,
              save_labels=args.save_labels, colors=args.colors, dither=args.dither,
              resize=args.resize, overshoot=args.overshoot, merge=args.merge,
              quick=args.quick, entire=args.entire)

if __name__ == '__main__':
    main()
