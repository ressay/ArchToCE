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
        firstaxis = None
        secondaxis = None
        for axis in self.axes:
            p=Point(axis.coords[0])
            for otheraxis in self.axes:
                otherp=Point(otheraxis.coords[0])
                if abs(p.y - otherp.y) < self.hminDist and p.y - otherp.y!=0:
                    self.hminDist=abs(p.y-otherp.y)
                    firstaxis=axis
                    secondaxis=otheraxis
        return self.hminDist, firstaxis,secondaxis

    def HmaximumDistance(self,uy,dy):
        distances=[]
        points=[]
        points.append(uy)
        for axis in self.axes:
            points.append(Point(axis.coords[0]).y)
        points.append(dy)
        points.sort()
        for p in points:
            ind = points.index(p)
            if ind == 0:
                op = points[ind+1]
                dist = abs(p-op)
            elif ind == len(points)-1:
                op = points[ind-1]
                dist = abs(p-op)
            else:
                op1 = points[ind-1]
                op2 = points[ind+1]
                dist=max(abs(p-op1),abs(p-op2))

            if dist not in distances: distances.append(dist)

        self.hmaxDist=max(distances)
        return self.hmaxDist

    def VminimumDistance(self):
        self.vminDist = self.axes[0].length
        firstaxis = None
        secondaxis = None
        for axis in self.axes:
            p=Point(axis.coords[0])
            for otheraxis in self.axes:
                otherp=Point(otheraxis.coords[0])
                if abs(p.x - otherp.x) < self.vminDist and p.x - otherp.x!=0:
                    self.vminDist=abs(p.x-otherp.x)
                    firstaxis = axis
                    secondaxis = otheraxis
        return self.vminDist, firstaxis,secondaxis

    def VmaximumDistance(self,rx,lx):
        distances = []
        points = []
        points.append(lx)
        for axis in self.axes:
            points.append(Point(axis.coords[0]).x)
        points.append(rx)
        points.sort()
        for p in points:
            ind = points.index(p)
            if ind == 0:
                op = points[ind + 1]
                dist = abs(p - op)
            elif ind == len(points) - 1:
                op = points[ind - 1]
                dist = abs(p - op)
            else:
                op1 = points[ind - 1]
                op2 = points[ind + 1]
                dist = max(abs(p - op1), abs(p - op2))

            if dist not in distances: distances.append(dist)

        self.vmaxDist=max(distances)
        return self.vmaxDist

    def HDistanceCondition(self,uy,dy):
        hmindist,firstaxis,secondaxis = self.HminimumDistance()
        hmaxdist = self.HmaximumDistance(uy,dy)
        i=0
        if hmindist > 2.5:
            if hmaxdist < 6:
                i=2
                Result  = True
            else:
                i=1
                Result= False
        else:
            Result = False
        return Result,firstaxis,secondaxis,i

    def VDistanceCondition(self,R_x,L_x):
        vmindist, firstaxis, secondaxis = self.VminimumDistance()
        vmaxdist = self.VmaximumDistance(R_x,L_x)
        i = 0
        if vmindist > 2.5:
            if vmaxdist < 6:
                i = 2
                Result = True
            else:
                i = 1
                Result = False
        else:
            Result = False
        return Result, firstaxis, secondaxis, i

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




