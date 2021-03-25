# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Show2DWindowMod.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(845, 679)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.loadFile = QtWidgets.QPushButton(self.centralwidget)
        self.loadFile.setGeometry(QtCore.QRect(630, 20, 96, 32))
        self.loadFile.setObjectName(_fromUtf8("loadFile"))
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(590, 140, 181, 331))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.selectedFileLabel = QtWidgets.QLabel(self.centralwidget)
        self.selectedFileLabel.setGeometry(QtCore.QRect(630, 70, 111, 20))
        self.selectedFileLabel.setObjectName(_fromUtf8("selectedFileLabel"))
        self.viewsLabel = QtWidgets.QLabel(self.centralwidget)
        self.viewsLabel.setGeometry(QtCore.QRect(660, 110, 41, 20))
        self.viewsLabel.setObjectName(_fromUtf8("viewsLabel"))
        self.showLower = QtWidgets.QPushButton(self.centralwidget)
        self.showLower.setGeometry(QtCore.QRect(620, 490, 111, 32))
        self.showLower.setObjectName(_fromUtf8("showLower"))
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 541, 521))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.sol2 = QtWidgets.QPushButton(self.centralwidget)
        self.sol2.setGeometry(QtCore.QRect(150, 550, 111, 32))
        self.sol2.setObjectName(_fromUtf8("sol2"))
        self.sol1 = QtWidgets.QPushButton(self.centralwidget)
        self.sol1.setGeometry(QtCore.QRect(10, 550, 111, 32))
        self.sol1.setObjectName(_fromUtf8("sol1"))
        self.merge = QtWidgets.QPushButton(self.centralwidget)
        self.merge.setGeometry(QtCore.QRect(300, 550, 111, 32))
        self.merge.setObjectName(_fromUtf8("merge"))
        self.cross = QtWidgets.QPushButton(self.centralwidget)
        self.cross.setGeometry(QtCore.QRect(450, 550, 111, 32))
        self.cross.setObjectName(_fromUtf8("cross"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 845, 28))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.loadFile.setText(_translate("MainWindow", "Load file", None))
        self.selectedFileLabel.setText(_translate("MainWindow", "No file selected", None))
        self.viewsLabel.setText(_translate("MainWindow", "Views", None))
        self.showLower.setText(_translate("MainWindow", "showLower", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))
        self.sol2.setText(_translate("MainWindow", "Solution2", None))
        self.sol1.setText(_translate("MainWindow", "Solution1", None))
        self.merge.setText(_translate("MainWindow", "GA", None))
        self.cross.setText(_translate("MainWindow", "Cross", None))

