from Skeleton.PolySkeleton import PolySkeleton


class SlabSkeleton(PolySkeleton):
    def __init__(self, poly):
        super(SlabSkeleton, self).__init__(poly)

    def copy(self):
        slab = SlabSkeleton(self.poly.copy())
        slab.evalData = self.evalData
        return slab

    @staticmethod
    def createSkeletonFromSlab(slab):
        return SlabSkeleton(slab.getBasePolygon())

