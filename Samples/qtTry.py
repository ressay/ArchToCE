import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):

    draw = False

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()
        self.test = self

    def initUI(self):

        self.setGeometry(400, 400, 400, 400)

        # qbtn = QtGui.QPushButton('Paint', self)
        # qbtn.clicked.connect(self.buttn)
        # qbtn.resize(qbtn.sizeHint())
        # qbtn.move(50, 50)

        # self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Paint')
        self.show()


    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self, qp):
        qp.setBrush(QtGui.QColor(000, 000, 255))
        qp.drawRect(0, 0, 400, 200)
        self.update()

    @QtCore.pyqtSlot()
    def buttn(self):
        self.draw = True



def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()