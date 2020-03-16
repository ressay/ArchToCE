from shapely.geometry import Point,Polygon
import math
from math import atan2, sin, cos, sqrt, pi, degrees



class Pnt(object):

    def __init__(self,x,y):
        super(Pnt, self).__init__()
        self.pnt = Point(x,y)

    def x(self):
        return self.pnt.x

    def y(self):
        return self.pnt.y

    def magn(self):
        return math.sqrt(self.x()*self.x()+self.y()*self.y())


    def isParallel(self,point,threshold=0):
        if abs(self.y()) <= threshold:
            return abs(point.y()) <= threshold
        if abs(point.y()) <=threshold:
            return False
        return abs(self.x()/self.y() - point.x()/point.y()) <= threshold


    def isInPolygon(self,poly):
        return poly.containsPoint(self)



    def scale(self,r):
        self.pnt = Point(self.pnt.x*r, self.pnt.y*r)
        return self

    def resize(self,size):
        self.scale(1/self.magn()).scale(size)
        return self

    def move(self,x,y):
        self.pnt = Point(self.pnt.x+x,self.pnt.y+y)
        return self

    def minus(self,pnt):
        return Pnt(self.x()-pnt.x(),self.y()-pnt.y())

    def plus(self,pnt):
        return Pnt(self.x()+pnt.x(),self.y()+pnt.y())

    def copy(self):
        return Pnt(self.x(),self.y())

    def __copy__(self):
        return self.copy()

    def __add__(self, other):
        return self.plus(other)

    def __sub__(self, other):
        return self.minus(other)

    def __mul__(self, other):
        return self.copy().scale(other)

    def __div__(self, other):
        return self*(1.0/other)

    def __str__(self):
        return "("+str(self.x())+","+str(self.y())+")"

    @staticmethod
    def createPointFromShapely(point):
        return Pnt(point.x,point.y)


def area(pts):
    'Area of cross-section.'

    if pts[0] != pts[-1]:
        pts = pts + pts[:1]
    x = [c[0] for c in pts]
    y = [c[1] for c in pts]
    s = 0
    for i in range(len(pts) - 1):
        s += x[i] * y[i + 1] - x[i + 1] * y[i]
    return s / 2


def centroid(pts):
    'Location of centroid.'

    if pts[0] != pts[-1]:
        pts = pts + pts[:1]
    x = [c[0] for c in pts]
    y = [c[1] for c in pts]
    sx = sy = 0
    a = area(pts)
    for i in range(len(pts) - 1):
        sx += (x[i] + x[i + 1]) * (x[i] * y[i + 1] - x[i + 1] * y[i])
        sy += (y[i] + y[i + 1]) * (x[i] * y[i + 1] - x[i + 1] * y[i])
    return sx / (6 * a), sy / (6 * a)


def inertia(pts):
    'Moments and product of inertia about centroid.'

    if pts[0] != pts[-1]:
        pts = pts + pts[:1]
    x = [c[0] for c in pts]
    y = [c[1] for c in pts]
    sxx = syy = sxy = 0
    a = area(pts)
    cx, cy = centroid(pts)
    for i in range(len(pts) - 1):
        sxx += (y[i] ** 2 + y[i] * y[i + 1] + y[i + 1] ** 2) * (x[i] * y[i + 1] - x[i + 1] * y[i])
        syy += (x[i] ** 2 + x[i] * x[i + 1] + x[i + 1] ** 2) * (x[i] * y[i + 1] - x[i + 1] * y[i])
        sxy += (x[i] * y[i + 1] + 2 * x[i] * y[i] + 2 * x[i + 1] * y[i + 1] + x[i + 1] * y[i]) * (
        x[i] * y[i + 1] - x[i + 1] * y[i])
    return sxx / 12 - a * cy ** 2, syy / 12 - a * cx ** 2, sxy / 24 - a * cx * cy

class Poly(object):



    def __init__(self,pts):
        super(Poly, self).__init__()
        self.points = pts
        self.poly = Polygon
        self.updatePolygon()

    def move(self,x,y):
        for pt in self.points:
            pt.move(x,y)
        self.updatePolygon()

    def scale(self,r):
        for pt in self.points:
            pt.scale(r)
        self.updatePolygon()


    def updatePolygon(self):
        self.poly = Polygon([(pnt.x(), pnt.y()) for pnt in self.points])
        # self.poly = Polygon([(1,2),(1,1),(5,5)])

    def containsPoint(self,pnt):
        self.poly.contains(pnt.pnt)

    def intersects(self,poly):
        return self.poly.intersects(poly.poly)

    def intersection(self,poly):
        if not self.intersects(poly):
            return None
        try:
            poly = self.poly.intersection(poly.poly)
            if type(poly) is Polygon:
                return Poly(Poly.getPointsFromShapelyPoly(poly))
        except Exception:
            return None
        return None

    def union(self,poly): #does not return a Poly object
        return self.poly.union(poly.poly)

    def subtractPoly(self,poly):
        spoints = list(self.points)
        if len(self.points) > 4:
            pnts = self.points
            size = len(pnts)
            for i in range(size):
                p1,p2 = pnts[(i-1)%size], pnts[(i+1)%size]
                vec1 = pnts[i] - p1
                vec2 = p2 - pnts[i]
                if vec1.isParallel(vec2,0.05):
                    spoints.remove(pnts[i])
            if len(spoints) > 4:
                return [self]
        def getTopLeft(points):
            minY = min([pnt.y() for pnt in points])
            minX = None
            minPnt = None
            for pnt in points:
                if pnt.y() == minY:
                    if not minPnt:
                        minPnt = pnt
                        minX = pnt.x()
                    if pnt.x() < minX:
                        minPnt = pnt
                        minX = pnt.x()
            return minPnt

        pntM = getTopLeft(spoints)
        indM = [i for i, pnt in enumerate(spoints)
                if pnt.x() == pntM.x() and pnt.y() == pntM.y()][0]
        vecL = spoints[(indM + 1) % len(spoints)] - spoints[indM]
        vecW = spoints[(indM - 1) % len(spoints)] - spoints[indM]
        if vecW.magn() > vecL.magn():
            vecL, vecW = vecW, vecL
        pPntM = None
        minS = None
        for pnt in poly.points:
            vec = pnt - pntM
            if vec.isParallel(vecL):
                if not pPntM:
                    pPntM = pnt
                    minS = vec.magn()
                elif minS > vec.magn():
                    pPntM = pnt
                    minS = vec.magn()
        if not pPntM:
            # from UI import Plotter
            # from matplotlib import pyplot as plt
            # print("ERROR GEOM2D: NO PARALLELISM")
            # print(self)
            # print(poly)
            # Plotter.plotPolys([self],1)
            # Plotter.plotPolys([poly], 2)
            # Plotter.plotPolys([self,poly], 2)
            # plt.show()
            return [self]
        # pPntM = getTopLeft(poly.points)

        pIndM = [i for i, pnt in enumerate(poly.points)
                 if pnt.x() == pPntM.x() and pnt.y() == pPntM.y()][0]

        pvecL = poly.points[(pIndM+1)%len(poly.points)] - poly.points[pIndM]
        pvecW = poly.points[(pIndM-1)%len(poly.points)] - poly.points[pIndM]
        # print(vecL)
        # print(vecW)
        # print(pvecL)
        # print(pvecW)
        if pvecW.isParallel(vecL,0.05):
            pvecW,pvecL = pvecL,pvecW
        if not pvecL.isParallel(vecL,0.05):
            print("ERROR GEOM2D SUBTRACTPOLY: NOT PARALLEL, THEY SHOULD BE PARALLEL!")
            return [self]
        vecp = pPntM - pntM
        if pntM.x() == pPntM.x() and pntM.y() == pPntM.y():
            if pvecL.magn() == vecL.magn():
                # print("REMOVING IT ALL!!!")
                # print(self)
                # print(poly)
                return []
            return [Poly([pPntM+pvecL,pPntM+pvecL+pvecW,pntM+vecL+pvecW,pntM+vecL])]
        if vecp.magn()+pvecL.magn() == vecL.magn():
            return [Poly([pntM,pPntM,pPntM+pvecW,pntM+pvecW])]
            # return [self]
        polys = [Poly([pntM,pPntM,pPntM+pvecW,pntM+pvecW]),
                Poly([pPntM+pvecL,pPntM+pvecL+pvecW,pntM+vecL+pvecW,pntM+vecL])]
        # print(polys[0])
        # print(polys[1])
        return polys
        # return [self]



    def copy(self):
        return Poly([pnt.copy() for pnt in self.points])

    def area(self):
        return self.poly.area

    def centroid(self):
        return self.poly.centroid

    def momentX(self):
        pts = [[p.x(), p.y()] for p in self.points][::-1]
        return inertia(pts)[0]

    def momentY(self):
        pts = [[p.x(), p.y()] for p in self.points][::-1]
        return inertia(pts)[1]

    def __copy__(self):
        return self.copy()

    def __str__(self):
        s = "polygon:\n"
        for pnt in self.points:
            s += str(pnt) + '\n'
        return s

    @staticmethod
    def getPointsFromShapelyPoly(polygon):
        pnts = []
        for pnt in polygon.exterior.coords:
            pnts.append(Pnt(pnt[0],pnt[1]))
        del pnts[-1]
        return pnts


class Ellip(object):

    def __init__(self,pnt,d1,d2=None):
        super(Ellip, self).__init__()
        self.pnt = pnt
        self.d1 = d1
        self.d2 = d2
        if not d2:
            self.d2 = d1

    def move(self, x, y):
        self.pnt.move(x,y)

    def scale(self,r):
        self.pnt.scale(r)
        self.d1 *= r
        self.d2 *= r