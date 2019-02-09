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
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelState = QtGui.QLabel(self.centralwidget)
        self.labelState.setStyleSheet(_fromUtf8("border-width: 2px;\n"
"background-color: rgb(170, 255, 255);\n"
"border-radius: 15px;\n"
"padding: 4px;"))
        self.labelState.setObjectName(_fromUtf8("labelState"))
        self.horizontalLayout.addWidget(self.labelState)
        self.pushButtonLog = QtGui.QPushButton(self.centralwidget)
        self.pushButtonLog.setStyleSheet(_fromUtf8("border-width: 2px;\n"
"border-radius: 15px;\n"
"padding: 4px;\n"
"background-color: rgb(255, 255, 127);"))
        self.pushButtonLog.setObjectName(_fromUtf8("pushButtonLog"))
        self.horizontalLayout.addWidget(self.pushButtonLog)
        self.pushButtonDel = QtGui.QPushButton(self.centralwidget)
        self.pushButtonDel.setStyleSheet(_fromUtf8("border-width: 2px;\n"
"background-color: rgb(255, 127, 127);\n"
"border-radius: 15px;\n"
"padding: 4px;"))
        self.pushButtonDel.setObjectName(_fromUtf8("pushButtonDel"))
        self.horizontalLayout.addWidget(self.pushButtonDel)
        self.pushButtonLive = QtGui.QPushButton(self.centralwidget)
        self.pushButtonLive.setStyleSheet(_fromUtf8("border-width: 2px;\n"
"border-radius: 15px;\n"
"padding: 4px;\n"
"background-color: rgb(170, 255, 127);"))
        self.pushButtonLive.setObjectName(_fromUtf8("pushButtonLive"))
        self.horizontalLayout.addWidget(self.pushButtonLive)
        self.pushButtonStop = QtGui.QPushButton(self.centralwidget)
        self.pushButtonStop.setStyleSheet(_fromUtf8("border-width: 2px;\n"
"border-radius: 15px;\n"
"padding: 4px;\n"
"background-color: rgb(255, 127, 127);"))
        self.pushButtonStop.setObjectName(_fromUtf8("pushButtonStop"))
        self.horizontalLayout.addWidget(self.pushButtonStop)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelCell = QtGui.QLabel(self.centralwidget)
        self.labelCell.setStyleSheet(_fromUtf8(""))
        self.labelCell.setObjectName(_fromUtf8("labelCell"))
        self.verticalLayout.addWidget(self.labelCell)
        self.tableCell = QtGui.QTableView(self.centralwidget)
        self.tableCell.setStyleSheet(_fromUtf8(""))
        self.tableCell.setObjectName(_fromUtf8("tableCell"))
        self.verticalLayout.addWidget(self.tableCell)
        self.labelTemp = QtGui.QLabel(self.centralwidget)
        self.labelTemp.setStyleSheet(_fromUtf8(""))
        self.labelTemp.setObjectName(_fromUtf8("labelTemp"))
        self.verticalLayout.addWidget(self.labelTemp)
        self.tableTemp = QtGui.QTableView(self.centralwidget)
        self.tableTemp.setStyleSheet(_fromUtf8(""))
        self.tableTemp.setObjectName(_fromUtf8("tableTemp"))
        self.verticalLayout.addWidget(self.tableTemp)
        self.labelMod = QtGui.QLabel(self.centralwidget)
        self.labelMod.setStyleSheet(_fromUtf8(""))
        self.labelMod.setObjectName(_fromUtf8("labelMod"))
        self.verticalLayout.addWidget(self.labelMod)
        self.tableMod = QtGui.QTableView(self.centralwidget)
        self.tableMod.setStyleSheet(_fromUtf8(""))
        self.tableMod.setObjectName(_fromUtf8("tableMod"))
        self.verticalLayout.addWidget(self.tableMod)
        self.labelCAN = QtGui.QLabel(self.centralwidget)
        self.labelCAN.setStyleSheet(_fromUtf8(""))
        self.labelCAN.setObjectName(_fromUtf8("labelCAN"))
        self.verticalLayout.addWidget(self.labelCAN)
        self.tableCAN = QtGui.QTableView(self.centralwidget)
        self.tableCAN.setStyleSheet(_fromUtf8(""))
        self.tableCAN.setObjectName(_fromUtf8("tableCAN"))
        self.verticalLayout.addWidget(self.tableCAN)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 38))
        self.menubar.setAutoFillBackground(False)
        self.menubar.setStyleSheet(_fromUtf8(""))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setStyleSheet(_fromUtf8(""))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionQuit)
        self.menuSettings.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.labelState.setText(_translate("MainWindow", "State: ", None))
        self.pushButtonLog.setText(_translate("MainWindow", "Log", None))
        self.pushButtonDel.setText(_translate("MainWindow", "Delete", None))
        self.pushButtonLive.setText(_translate("MainWindow", "Live", None))
        self.pushButtonStop.setText(_translate("MainWindow", "Stop", None))
        self.labelCell.setText(_translate("MainWindow", "Cell Data", None))
        self.labelTemp.setText(_translate("MainWindow", "Temperature Data", None))
        self.labelMod.setText(_translate("MainWindow", "Module Data", None))
        self.labelCAN.setText(_translate("MainWindow", "CAN Data", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))

