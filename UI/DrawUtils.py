import sys
from PyQt4 import QtGui, QtCore

from Geometry import ShapeToPoly


defaultColor = QtGui.QColor(220,220,220)

class cell(object):
    poly = None
    def __init__(self, c,p):
        self.color = c
        self.poly = p

    def drawPolygone(self, qp):
        qp.setBrush(self.color)

        qp.drawPolygon(self.createPoly())

    def createPoly(self):
        polygon = QtGui.QPolygonF()
        for pnt in self.poly.points:  # add the points of polygon
            polygon.append(QtCore.QPointF(pnt.x(),pnt.y()))

        return polygon


class Window(QtGui.QWidget):
    polys = []
    colors = []
    def __init__(self,polys,colors=None,rect=None):
        super(Window, self).__init__()
        if not rect:
            self.setGeometry(50, 50, 800, 600)
        else:
            self.setGeometry(rect)
        # self.setWindowTitle("PyQT tuts!")
        self.cells = []
        self.polys = polys
        if colors:
            self.colors = colors
        self.resizePolys()
        now = QtCore.QTime.currentTime()
        QtCore.qsrand(now.msec())
        self.createCells()

    def resizePolys(self):
        polygons = self.polys
        minX = min([pnt.x() for pnt in [pt for polygon in polygons for pt in polygon.points]])
        maxX = max([pnt.x() for pnt in [pt for polygon in polygons for pt in polygon.points]])
        minY = min([pnt.y() for pnt in [pt for polygon in polygons for pt in polygon.points]])
        maxY = max([pnt.y() for pnt in [pt for polygon in polygons for pt in polygon.points]])

        x,y,w,h = self.geometry().getRect()
        x2 = x+w
        y2 = y+h
        print(str(x) + "," + str(y)+ "  " + str(x2) + "," + str(y2))
        print(str(minX) + "," + str(minY)+ "  " + str(maxX) + "," + str(maxY))
        w2 = maxX - minX
        h2 = maxY - minY
        r1 = w/w2
        r2 = h/h2
        r = min([r1,r2])
        for pol in self.polys:
            pol.move(-minX,-minY)
            pol.scale(r)


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



    def createCells(self):
        for i in range(len(self.polys)-len(self.colors)):
            self.colors.append(defaultColor)
        for polygon,color in zip(self.polys,self.colors):
            self.cells.append(cell(color,polygon))
        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        # qp.scale(30,30)
        for c in self.cells:
            c.drawPolygone(qp)


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