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

def solve_rounds(pixels, number_of_cans, max_pixels_per_can):
    idx = index.Index()

    # Insert all pixels into the rtree
    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            idx.insert(pixels[y][x], (x, y, x, y), obj=[(x, y, pixels[y][x])])
    w, h = pixels.shape()

    # left bottom right top
    bbox = (0, 0, h, w)

    performed_merge = True
    level = 0
    num_clusters = h*w  # TODO: don't count empty pixels
    max_per_cluster = 100
    while performed_merge:
        performed_merge = False

        objs = idx.intersection(bbox, objects=True)
        # random dist
        rdist = random.sample(objs, max_per_cluster)

        # cluster into next level
        next_tree = idx.Index()
        for center in rdist:
            new_clusters = [[] for _ in range(number_of_cans)]
            for cluster in idx.nearest(center.bbox, max_per_cluster, objects=True):
                # (x, y, color)
                obj = cluster.object
                if len(obj) < max_per_cluster:
                    new_clusters[cluster.id].append(obj)
                    performed_merge = True
                idx.delete(cluster.id, cluster.bbox)

            for k, v in enumerate(new_clusters):
                x, y, _ = map(lambda x: sum(x)/len(x), zip(*new_clusters))
                next_tree.insert(k, (x, y, x, y), obj=v)

        level += 1

def main():
    parser = argparse.ArgumentParser('venus')
    parser.add_argument('-i', '--image', type=str)
    parser.add_argument('-m', '--max-pixels-per-can', type=int, default=100)
    parser.add_argument('-n', '--number-of-cans', type=int, default=4)

    args = parser.parse_args()

if __name__ == '__main__':
    main()
