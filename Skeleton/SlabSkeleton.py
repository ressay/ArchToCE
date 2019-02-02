from Skeleton.PolySkeleton import PolySkeleton


class SlabSkeleton(PolySkeleton):
    def __init__(self, poly,slab):
        super(SlabSkeleton, self).__init__(poly)
        self.slab = slab

    def copy(self):
        slab = SlabSkeleton(self.poly.copy(),self.slab)
        slab.evalData = self.evalData
        return slab

    @staticmethod
    def createSkeletonFromSlab(slab):
        return SlabSkeleton(slab.getBasePolygon(),slab)

