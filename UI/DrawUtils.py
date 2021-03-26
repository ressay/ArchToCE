import sys
from PyQt5 import QtGui, QtCore, QtWidgets

from Geometry import ShapeToPoly


defaultColor = QtGui.QColor(220,220,220)
color2 = QtGui.QColor(220,220,0)

class drawable(object):
    def __init__(self):
        super(drawable, self).__init__()

    def draw(self,qp):
        pass


class ellipse(drawable):
    def __init__(self,pnt,d,c):
        super(ellipse, self).__init__()
        self.pnt = pnt
        self.d = d
        self.color = c

    def drawCircle(self, qp):
        qp.setBrush(self.color)
        p = self.pnt
        qp.drawEllipse(p.x(),p.y(),self.d,self.d)

    def draw(self, qp):
        super(ellipse, self).draw(qp)
        self.drawCircle(qp)


class cell(drawable):
    poly = None
    def __init__(self, c, p):
        super(cell, self).__init__()
        self.color = c
        self.poly = p

    def draw(self, qp):
        super(cell, self).draw(qp)
        self.drawPolygone(qp)

    def drawPolygone(self, qp):
        qp.setBrush(self.color)
        qp.drawPolygon(self.createPoly())



    def createPoly(self):
        polygon = QtGui.QPolygonF()
        for pnt in self.poly.points:  # add the points of polygon
            polygon.append(QtCore.QPointF(pnt.x(),pnt.y()))

        return polygon



class Window(QtWidgets.QWidget):
    polys = []
    colorsP = []
    def __init__(self,polys,rect=None,ellipses=None):
        super(Window, self).__init__()
        if not rect:
            self.setGeometry(50, 50, 800, 600)
        else:
            self.setGeometry(rect)
        # self.setWindowTitle("PyQT tuts!")
        self.drawables = []
        self.ellipses = []
        self.polys = []
        self.colorsE = []
        self.colorsP = []

        self._setPolys(polys)
        self._setEllipses(ellipses)
        self.resizePolys()
        now = QtCore.QTime.currentTime()
        QtCore.qsrand(now.msec())
        self.createShapes()

    def resizePolys(self):
        polygons = self.polys
        minX = min([pnt.x() for pnt in [pt for polygon in polygons for pt in polygon.points]])
        maxX = max([pnt.x() for pnt in [pt for polygon in polygons for pt in polygon.points]])
        minY = min([pnt.y() for pnt in [pt for polygon in polygons for pt in polygon.points]])
        maxY = max([pnt.y() for pnt in [pt for polygon in polygons for pt in polygon.points]])

        x,y,w,h = self.geometry().getRect()
        x2 = x+w
        y2 = y+h
        print((str(x) + "," + str(y)+ "  " + str(x2) + "," + str(y2)))
        print((str(minX) + "," + str(minY)+ "  " + str(maxX) + "," + str(maxY)))
        w2 = maxX - minX
        h2 = maxY - minY
        r1 = w/w2
        r2 = h/h2
        r = min([r1,r2])
        for pol in self.polys:
            pol.move(-minX,-minY)
            pol.scale(r)
        for ell in self.ellipses:
            ell.move(-minX,-minY)
            ell.scale(r)


        minY = min([pnt.y() for pnt in [pt for polygon in polygons for pt in polygon.points]])
        maxY = max([pnt.y() for pnt in [pt for polygon in polygons for pt in polygon.points]])
        minX = min([pnt.x() for pnt in [pt for polygon in polygons for pt in polygon.points]])
        maxX = max([pnt.x() for pnt in [pt for polygon in polygons for pt in polygon.points]])

        w2 = maxX - minX
        h2 = maxY - minY
        mvy = (h - h2) / 2
        mvx = (w - w2) / 2
        for pol in self.polys:
            pol.move(mvx,mvy)
        for ell in self.ellipses:
            ell.move(mvx,mvy)

    def _setPolys(self,polys):
        polys, colors = polys
        self.polys = polys
        if colors:
            self.colorsP = colors

    def _setEllipses(self,ellipses):
        if ellipses:
            ellipses, colors = ellipses
            self.ellipses = ellipses
            if colors:
                self.colorsE = colors

    def createCells(self):
        for i in range(len(self.polys)-len(self.colorsP)):
            self.colorsP.append(defaultColor)
        for polygon,color in zip(self.polys, self.colorsP):
            self.drawables.append(cell(color,polygon))

    def createEllipses(self):
        for i in range(len(self.ellipses)-len(self.colorsE)):
            self.colorsE.append(defaultColor)
        for ell,color in zip(self.ellipses, self.colorsE):
            self.drawables.append(ellipse(ell.pnt,ell.d1,color))

    def createShapes(self):
        self.createCells()
        self.createEllipses()
        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        # qp.scale(30,30)
        for c in self.drawables:
            c.draw(qp)



from Ifc import IfcUtils

if __name__ == '__main__':


    wall_shapes = IfcUtils.getWallShapesFromIfc("IFCFiles/projet.ifc")
    # wall_shapes = IfcUtils.getSlabShapesFromIfc("IFCFiles/projet.ifc")
    shapes = []
    for wall, shape in wall_shapes:
        shapes.append(shape)

    polygons = ShapeToPoly.getShapesBasePolygons(shapes)
    lx = min([pnt.x() for pnt in [pt for polygon in polygons for pt in polygon.points]])
    ly = min([pnt.y() for pnt in [pt for polygon in polygons for pt in polygon.points]])

    for polygon in polygons:
        polygon.move(-lx+10, -ly+10)
        # print ("polygon is: ")
        # for pnt in polygon.points:
        #     print("point is: (%.2f, %.2f) " % (pnt.x, pnt.y))

    # IfcUtils.displayShapes(shapes)
    app = QtGui.QApplication(sys.argv)
    w = Window(polygons)
    w.show()
    sys.exit(app.exec_())