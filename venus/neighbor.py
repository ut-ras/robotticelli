class Index(object):
    def __init__(self,  *args, **kwargs):
        self.points = []
        self.deleted = set()

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
        for i in filtered:
            if i[0] not in self.deleted:
                yield i

    def delete(self, xytag):
        self.deleted.add(xytag)

    def getpoints(self, tag):
        for i in filter(lambda x: x[0][2] == tag, self.points):
            if i[0] not in self.deleted:
                yield i

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
