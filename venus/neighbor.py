class Index(object):
    def __init__(self,  *args, **kwargs):
        self.points = []

    def __len__(self,  *args, **kwargs):
        return len(self.points)

    def insert(self, xytag, obj):
        self.points.append((xytag, obj))

    def nearest(self, xytag, num_results=1):
        def distance(point):
            point = point[0]
            return (((point[0] - xytag[0]) ** 2) +
                    ((point[1] - xytag[1]) ** 2))

        filtered = filter(lambda x: x[0][2] == xytag[2], self.points)
        filtered.sort(key=distance)
        return filtered[:num_results]

    def delete(self, xytag):
        idxs = [i for i, p in enumerate(self.points) if p[0] == xytag]
        for i in reversed(idxs):
            self.points.pop(i)

    def getpoints(self, tag):
        return filter(lambda x: x[0][2] == tag, self.points)

    def valid(self):
        return True

if __name__ == '__main__':
    idx = Index()
    idx.insert((0, 0, 0), set([(0, 0, 0)]))
    idx.insert((0, 1, 0), set([(0, 1, 0)]))
    idx.insert((1, 0, 0), set([(1, 0, 0)]))
    idx.insert((1, 1, 0), set([(1, 1, 0)]))
    print(idx.nearest((0, 0, 0), 4))
    print(idx.nearest((0, 0, 0), 3))
    idx.delete((0, 1, 0))
    idx.insert((1, 1, 1), set([(1, 1, 1)]))
    print(idx.getpoints(0))
