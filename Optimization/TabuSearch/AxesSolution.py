from shapely.geometry import Point

class AxesSolution(object):

    # this represents a solution. it contains axes.
    # feel free to add other attributes that you see necessary to evaluate the solution.
    def __init__(self, axes: list) -> None:
        super().__init__()

        self.axes = axes
        self.intersections= None
        self.hminDist=None
        self.hmaxDist=None
        self.vmindist=None

        # add your attributes here:

        #self.attribute = ...


    def HminimumDistance(self):
        self.hminDist = self.axes[0].length
        for axis in self.axes:
            p=Point(axis.coords[0])
            for otheraxis in self.axes:
                otherp=Point(otheraxis.coords[0])
                if abs(p.y - otherp.y) < self.hminDist and p.y - otherp.y!=0:
                    self.hminDist=abs(p.y-otherp.y)
        print("Distance", self.hminDist)
        return self.hminDist

