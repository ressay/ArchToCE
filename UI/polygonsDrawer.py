from PyQt4 import QtGui,QtCore
import scrollable

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
            polygon.append(QtCore.QPointF(pnt.x,pnt.y))

        return polygon


class PolysWidg(QtGui.QWidget, scrollable.Ui_Form):
    levels = []
    viewerTabs = {}
    def __init__(self, parent=None):
        super(PolysWidg, self).__init__(parent)
        self.setupUi(self)

