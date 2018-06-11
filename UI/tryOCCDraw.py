import sys
from OCC.Display.qtDisplay import qtViewer3d
from PyQt4 import QtGui,QtCore


from UI.test2 import AppGUI


class ViewerMainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.graphicsView = MyQtViewer3d(self.viewer_centralwidget)  # derived from qtViewer3d
        self._graphicsinitialized = False
        self.connect(self.graphicsView, QtCore.SIGNAL("sigGraphicsInitialised"), self.slotGraphicsInitialised)

    def AssertGraphicsInitialized(self):
        if not self._graphicsinitialized:
            self.graphicsView.InitDriver()

    def slotGraphicsInitialised(self):
        self._graphicsinitialized = True

        self.SetDefaultBackground()


class MyQtViewer3d(qtViewer3d):
    def InitDriver(self):
        qtViewer3d.InitDriver(self)
        self._display.EnableAntiAliasing()
        self.SetupTrihedron()
        self.context = self._display.GetContext().GetObject()  # AIS_InteractiveContext
        self.emit(QtCore.SIGNAL("sigGraphicsInitialised"), ())

# Which Qt signal you could use to trigger a call to AssertGraphicsInitialized depends on your application of course.
# You might also try to simply override the paintEvent method:

    def paintEvent(self, event):
        QtGui.QMainWindow.paintEvent(self, event)
        self. AssertGraphicsInitialized()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = AppGUI()
    win.show()
    win.modelTab.InitDriver()
    win.modelTab._display.Test()
    app.exec_()