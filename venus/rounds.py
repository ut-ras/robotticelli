# In this step, we need to divide the image into disjoint sets. Each set
# must satisfy the following properites:
#       - contain at most N colors, where N is the number of cans
#       - for each color, have at most (max pixels per can) pixels
# The ideal solution will form a set that maximizes the number of pixels
# sprayed and minimize distance between pixels. It's important to create
# a set of adjacent pixels rather than a sparse array.

# Inputs:
#       - pixels                numpy.ndarray of Integers
#       - max pixels per can    Integer
#       - number of cans        Integer
# Outputs:
#       - set(([(x, y, can number)], [(color, can number)]))

from rtree import index
import random
import argparse
import numpy as np
import math

def solve_rounds(pixels, number_of_cans, max_pixels_per_can, max_per_cluster=100):
    idx = index.Index()

    # Insert all pixels into the rtree
    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            idx.insert(pixels[y][x], (x, y, x, y), obj=set([(x, y, pixels[y][x])]))
    w, h = pixels.shape

    # left bottom right top
    bbox = (0, 0, h, w)

    performed_merge = True
    level = 0
    num_clusters = h*w  # TODO: don't count empty pixels
    while performed_merge:
        performed_merge = False

        objs = list(idx.intersection(bbox, objects=True))

        # cluster into next level
        next_tree = index.Index()
        num_pixels = np.bincount(pixels.reshape(h*w))
        for color in range(number_of_cans):
            # random dist
            color_map = filter(lambda x: x.id == color, objs)
            pop = int(math.ceil(1.0*num_pixels[color]/max_per_cluster))
            rdist = random.sample(color_map, pop)
            for center in rdist:
                new_cluster = center.object
                idx.delete(center.id, center.bbox)
                for cluster in idx.nearest(center.bbox, max_per_cluster, objects=True):
                    obj = cluster.object
                    if len(obj | new_cluster) < max_per_cluster:
                        performed_merge = bool(obj - new_cluster)
                        new_cluster.union(obj)
                        idx.delete(cluster.id, cluster.bbox)

                # find new center of cluster
                if new_cluster:
                    print(new_cluster)
                    x, y, _ = map(lambda x: sum(x)/len(x), zip(*new_cluster))
                    next_tree.insert(color, (x, y, x, y), obj=new_cluster)

        idx = next_tree
        level += 1
    print(list(x.object for x in idx.intersection(bbox, objects=True)))
    return list(x.object for x in idx.intersection(bbox, objects=True))

def main():
    parser = argparse.ArgumentParser('venus')
    parser.add_argument('-i', '--image', type=str)
    parser.add_argument('-m', '--max-pixels-per-can', type=int, default=100)
    parser.add_argument('-n', '--number-of-cans', type=int, default=4)

    args = parser.parse_args()
    sample = [
        [9, 9, 9, 9, 9, 1, 0, 9],
        [9, 9, 9, 9, 9, 1, 0, 0],
        [9, 9, 9, 9, 1, 1, 1, 1],
        [9, 9, 0, 1, 1, 9, 1, 9],
        [0, 0, 1, 1, 9, 9, 9, 9],
        [9, 9, 0, 9, 9, 0, 0, 0],
        [9, 9, 9, 9, 9, 0, 0, 0],
        [9, 9, 9, 9, 9, 1, 1, 1]
    ]
    cluster_size = 3
    num_cans = 1
    solve_rounds(np.array(sample), num_cans, 100, cluster_size)

if __name__ == '__main__':
    main()
