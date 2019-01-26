# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bmsgui.ui'
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
        MainWindow.resize(1440, 1080)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableCell = QtGui.QTableView(self.centralwidget)
        self.tableCell.setObjectName(_fromUtf8("tableCell"))
        self.verticalLayout.addWidget(self.tableCell)
        self.tableTemp = QtGui.QTableView(self.centralwidget)
        self.tableTemp.setObjectName(_fromUtf8("tableTemp"))
        self.verticalLayout.addWidget(self.tableTemp)
        self.tableView_4 = QtGui.QTableView(self.centralwidget)
        self.tableView_4.setObjectName(_fromUtf8("tableView_4"))
        self.verticalLayout.addWidget(self.tableView_4)
        self.tableCAN = QtGui.QTableView(self.centralwidget)
        self.tableCAN.setObjectName(_fromUtf8("tableCAN"))
        self.verticalLayout.addWidget(self.tableCAN)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 38))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuConnect = QtGui.QMenu(self.menubar)
        self.menuConnect.setObjectName(_fromUtf8("menuConnect"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionConnect = QtGui.QAction(MainWindow)
        self.actionConnect.setObjectName(_fromUtf8("actionConnect"))
        self.menuConnect.addAction(self.actionConnect)
        self.menubar.addAction(self.menuConnect.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuConnect.setTitle(_translate("MainWindow", "Tab", None))
        self.actionConnect.setText(_translate("MainWindow", "Connect", None))

