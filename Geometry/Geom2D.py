from shapely.geometry import Point,Polygon

class Pnt(object):
    pnt = Point

    def __init__(self,x,y):
        super(Pnt, self).__init__()
        self.pnt = Point(x,y)

    def x(self):
        return self.pnt.x

    def y(self):
        return self.pnt.y

    def move(self,x,y):
        self.pnt = Point(self.pnt.x+x,self.pnt.y+y)

    def isInPolygon(self,poly):
        poly.containsPoint(self)

    def scale(self,r):
        self.pnt = Point(self.pnt.x*r, self.pnt.y*r)



class Poly(object):
    poly = Polygon
    points = []

    def __init__(self,pts):
        super(Poly, self).__init__()
        self.points = pts
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