import sys
from OCC.Display.backend import load_backend
from PyQt4 import QtGui

from PyQt4.QtGui import QWidget, QFormLayout, QLabel

import Show2DWindow
from Geometry import ShapeToPoly
from Samples.DrawUtils import Window
from Structure.Level import Level
from Ifc import IfcUtils

load_backend("qt-pyqt4")   #here you need to tell OCC.Display to load qt4 backend

class TryApp(QtGui.QMainWindow, Show2DWindow.Ui_MainWindow):
    model = QtGui.QStandardItemModel()
    levels = []
    viewerTabs = {}
    def __init__(self, parent=None, wallShapes=None, slabShapes=None):
        super(TryApp, self).__init__(parent)
        self.setupUi(self)
        self.levels = Level.generateLevelsFromShapes(wallShapes,slabShapes)
        self.initListView()
        # self.loadFile.clicked.connect(self.browseFileCallBack)
        # self.openWin.clicked.connect(self.openWinCallBack)
        self.listView.setModel(self.model)
        self.listView.clicked.connect(self.listViewSelected)

        self.scrollTab = QtGui.QScrollArea()

        self.tabWidget.addTab(self.scrollTab, "upperView")

        self.addViewerTab("Walls")
        self.addViewerTab("Slabs")
        self.addViewerTab("All")
        self.addViewerTab("Selected")

        self.tabWidget.removeTab(0)
        self.tabWidget.removeTab(0)

        self.setViewerDisplay("Walls",wallShapes)
        self.setViewerDisplay("Slabs",slabShapes)
        all = wallShapes+slabShapes
        self.setViewerDisplay("All",all)


    def addViewerTab(self,name):
        from OCC.Display import qtDisplay
        self.viewerTabs[name] = qtDisplay.qtViewer3d(self)
        self.tabWidget.addTab(self.viewerTabs[name],name)
        self.viewerTabs[name].InitDriver()

    def setViewerDisplay(self,name,shapes):
        display = self.viewerTabs[name]._display
        display.EraseAll()
        self.initDisplayer(display,shapes)


    def initDisplayer(self,display,shapes):
        for shape in shapes:
            display.DisplayShape(shape)

    def initListView(self):
        i = 0
        for level in self.levels:
            item = QtGui.QStandardItem("level " + str(i))
            i += 1
            self.model.appendRow(item)

    def drawPolygons(self,shapes):
        from Geometry import ShapeToPoly
        polygons = ShapeToPoly.getShapesBasePolygons(shapes)
        if not len(polygons):
            return

        from UI.DrawUtils import Window
        self.scrollTab.setWidget(Window(polygons,self.scrollTab.geometry()))


    def listViewSelected(self, index):
        row = index.row()
        print ('selected item index found at %s with data: %s' % (index.row(), index.data().toString()))
        shapes = [wall.shape for wall in self.levels[row].walls]
        self.drawPolygons(shapes)
        shapes += [slab.shape for slab in self.levels[row].slabs]
        self.setViewerDisplay("Selected",shapes)







def createShapes(file):
    wall_shapes = IfcUtils.getWallShapesFromIfc(file)
    # wall_shapes = IfcUtils.getSlabShapesFromIfc("IFCFiles/projet.ifc")
    wShapes = []
    for wall, shape in wall_shapes:
        wShapes.append(shape)

    slab_shapes = IfcUtils.getSlabShapesFromIfc(file)
    sShapes = []
    for wall, shape in slab_shapes:
        sShapes.append(shape)

    return wShapes,sShapes

def main():
    file = "../IFCFiles/projet.ifc"
    wShapes,sShapes = createShapes(file)
    app = QtGui.QApplication(sys.argv)
    form = TryApp(wallShapes=wShapes,slabShapes=sShapes)
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
