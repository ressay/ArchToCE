# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Show2DWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(798, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.loadFile = QtGui.QPushButton(self.centralwidget)
        self.loadFile.setGeometry(QtCore.QRect(630, 20, 96, 32))
        self.loadFile.setObjectName(_fromUtf8("loadFile"))
        self.listView = QtGui.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(590, 140, 181, 331))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.selectedFileLabel = QtGui.QLabel(self.centralwidget)
        self.selectedFileLabel.setGeometry(QtCore.QRect(630, 70, 111, 20))
        self.selectedFileLabel.setObjectName(_fromUtf8("selectedFileLabel"))
        self.viewsLabel = QtGui.QLabel(self.centralwidget)
        self.viewsLabel.setGeometry(QtCore.QRect(660, 110, 41, 20))
        self.viewsLabel.setObjectName(_fromUtf8("viewsLabel"))
        self.openWin = QtGui.QPushButton(self.centralwidget)
        self.openWin.setGeometry(QtCore.QRect(620, 490, 111, 32))
        self.openWin.setObjectName(_fromUtf8("openWin"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 541, 521))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 798, 28))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.loadFile.setText(_translate("MainWindow", "Load file", None))
        self.selectedFileLabel.setText(_translate("MainWindow", "No file selected", None))
        self.viewsLabel.setText(_translate("MainWindow", "Views", None))
        self.openWin.setText(_translate("MainWindow", "Open Window", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))

