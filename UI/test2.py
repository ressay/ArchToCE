import sys
from PyQt4 import QtCore, QtGui
from OCC.Display.backend import load_backend
load_backend("qt-pyqt4")   #here you need to tell OCC.Display to load qt4 backend


class AppGUI(QtGui.QMainWindow):
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        # setup prefered interface
        self.treeArea = QtGui.QTreeWidget()
        self.textArea = QtGui.QTextEdit()
        self.viewArea = QtGui.QTabWidget()
        self.msgArea = QtGui.QTextBrowser()
        # Add tabs
        from OCC.Display import qtDisplay
        self.modelTab = qtDisplay.qtViewer3d(self)
        self.reportTab = QtGui.QTextBrowser()
        self.viewArea.addTab(self.modelTab, "Model")
        self.viewArea.addTab(self.reportTab, "Report")
        # Window area splitters
        self.vSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.vSplitter.addWidget(self.viewArea)
        self.vSplitter.addWidget(self.msgArea)
        self.hSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.hSplitter.addWidget(self.treeArea)
        self.hSplitter.addWidget(self.textArea)
        self.hSplitter.addWidget(self.vSplitter)
        # Assign mainwindow
        self.setCentralWidget(self.hSplitter)


if __name__ == '__main__':
    print("something!!")
    app = QtGui.QApplication(sys.argv)
    win = AppGUI()
    win.show()
    win.modelTab.InitDriver()
    win.modelTab._display.Test()
    app.exec_()