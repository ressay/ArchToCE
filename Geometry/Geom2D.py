from shapely.geometry import Point,Polygon
import math

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
        if self.y() <= threshold:
            return abs(point.y()) <= threshold
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

    def __str__(self):
        return "("+str(self.x())+","+str(self.y())+")"



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

    def copy(self):
        return Poly([pnt.copy() for pnt in self.points])

    def area(self):
        return self.poly.area

    def centroid(self):
        return self.poly.centroid

    def __copy__(self):
        return self.copy()