from shapely.geometry import Point
import random

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
        self.vmaxdist=None

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
        return self.hminDist

    def HmaximumDistance(self):
        distances=[]

        for axis in self.axes:
            p= Point(axis.coords[0]).y
            ind = self.axes.index(axis)
            if ind == 0:
                op= Point(self.axes[ind+1].coords[0]).y
                dist= abs(p-op)
            elif ind == len(self.axes)-1:
                op = Point(self.axes[ind-1].coords[0]).y
                dist= abs(p-op)
            else:
                op1= Point(self.axes[ind-1].coords[0]).y
                op2= Point(self.axes[ind+1].coords[0]).y
                dist=max(abs(p-op1),abs(p-op2))

            if dist not in distances: distances.append(dist)

        self.hmaxDist=max(distances)
        return self.hmaxDist

    def VminimumDistance(self):
        self.vminDist = self.axes[0].length
        for axis in self.axes:
            p=Point(axis.coords[0])
            for otheraxis in self.axes:
                otherp=Point(otheraxis.coords[0])
                if abs(p.x - otherp.x) < self.vminDist and p.x - otherp.x!=0:
                    self.vminDist=abs(p.x-otherp.x)
        return self.vminDist

    def VmaximumDistance(self):
        distances = []

        for axis in self.axes:
            p = Point(axis.coords[0]).x
            ind = self.axes.index(axis)
            if ind == 0:
                op = Point(self.axes[ind + 1].coords[0]).x
                dist = abs(p - op)
            elif ind == len(self.axes) - 1:
                op = Point(self.axes[ind - 1].coords[0]).x
                dist = abs(p - op)
            else:
                op1 = Point(self.axes[ind - 1].coords[0]).x
                op2 = Point(self.axes[ind + 1].coords[0]).x
                dist = max(abs(p - op1), abs(p - op2))

            if dist not in distances: distances.append(dist)

        self.vmaxDist=max(distances)
        return self.vmaxDist

    def HDistanceCondition(self):
        hmindist = self.HminimumDistance()
        hmaxdist = self.HmaximumDistance()
        if hmindist > 2.5 and hmaxdist < 6:
            return True
        else:
            return False

    def VDistanceCondition(self):
        vmindist = self.VminimumDistance()
        vmaxdist = self.VmaximumDistance()
        if vmindist > 2.5 and vmaxdist < 6:
            return True
        else:
            return False

    def AddrandomHAxis(self,Axes):
        test = False
        while not test:
            axis = random.choice(Axes[0])
            if axis not in self.axes[0]:
                self.axes[0].append(axis)
                test = True
        return self.axes[0]

    def AddrandomVAxis(self,Axes):
        test = False
        while not test:
            axis = random.choice(Axes[1])
            if axis not in self.axes[1]:
                self.axes[1].append(axis)
                test = True
        return self.axes[1]