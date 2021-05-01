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
                    firstaxis=axis
                    secondaxis=otheraxis
        return self.hminDist, firstaxis,secondaxis

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
                    firstaxis = axis
                    secondaxis = otheraxis
        return self.vminDist, firstaxis,secondaxis

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
        hmindist,firstaxis,secondaxis = self.HminimumDistance()
        hmaxdist = self.HmaximumDistance()
        if hmindist > 2.5 and hmaxdist < 6:
            return True, 0, 0
        else:
            return False, firstaxis, secondaxis

    def VDistanceCondition(self):
        vmindist, firstaxis, secondaxis = self.VminimumDistance()
        vmaxdist = self.VmaximumDistance()
        if vmindist > 2.5 and vmaxdist < 6:
            return True, 0, 0
        else:
            return False, firstaxis, secondaxis

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

    def get_DistancesFromEdges(self,R_x,L_x,U_y,D_y):
        Haxes=self.axes[0]
        Vaxes=self.axes[1]
        Ylist = []
        ylist = []
        Xlist = []
        xlist = []
        for axis in Haxes:
            Ylist.append(abs(U_y-Point(axis.coords[0]).y))
            ylist.append(abs(D_y-Point(axis.coords[0]).y))
        for axis in Vaxes:
            Xlist.append(abs(R_x-Point(axis.coords[0]).x))
            xlist.append(abs(L_x-Point(axis.coords[0]).x))
        Y=min(Ylist)
        y=min(ylist)
        X=min(Xlist)
        x=min(xlist)
        return x,X,y,Y



