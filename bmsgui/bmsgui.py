import design
import socket
import sys
from constants import *
from contextlib import closing
from os import path
from PyQt4 import QtCore, QtGui, QtSql

@fdec(dec)
class MyApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtGui.QMainWindow.__init__(self)
        design.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.connectdb = False
        self.dbname = ''
        self.db = None
        self.tableCellinit()
        self.tableTempinit()
        self.tableModinit()
        self.tableCANinit()
        self.actionNew.triggered.connect(self.new)
        self.actionOpen.triggered.connect(self.open)
        self.actionClose.triggered.connect(self.close)
        self.actionQuit.triggered.connect(self.closeEvent)
        #self.actionPreferences.triggered.connect()
    
    def tableCellinit(self, *args, **kwargs):
        self.modelCell = QtGui.QStandardItemModel()
        self.modelCell.setHorizontalHeaderLabels(headerCellh)
        self.modelCell.setVerticalHeaderLabels(headerCellv)
        rowCount, colCount = self.modelCell.rowCount(), self.modelCell.columnCount()
        for row in range(rowCount):
            for col in range(colCount -1):
                self.modelCell.setItem(row, col, QtGui.QStandardItem('-'))
            self.modelCell.setItem(row, colCount - 1, QtGui.QStandardItem('YYYY-mm-dd HH:MM:SS'))
        self.tableCell.setModel(self.modelCell)
        self.tableCell.horizontalHeader().setStretchLastSection(True)
        self.tableCell.horizontalHeader().resizeSections(3)
    
    def tableTempinit(self, *args, **kwargs):
        self.modelTemp = QtGui.QStandardItemModel()
        self.modelTemp.setHorizontalHeaderLabels(headerTemph)
        self.modelTemp.setVerticalHeaderLabels(headerTempv)
        rowCount, colCount = self.modelTemp.rowCount(), self.modelTemp.columnCount()
        for row in range(rowCount):
            for col in range(colCount -1):
                self.modelTemp.setItem(row, col, QtGui.QStandardItem('-'))
            self.modelTemp.setItem(row, colCount - 1, QtGui.QStandardItem('YYYY-mm-dd HH:MM:SS'))
        self.tableTemp.setModel(self.modelTemp)
        self.tableTemp.horizontalHeader().setStretchLastSection(True)
        self.tableTemp.horizontalHeader().resizeSections(3)
    
    def tableModinit(self, *args, **kwargs):
        #soc soh i
        pass

    def tableCANinit(self, *args, **kwargs):
        self.modelCAN = QtGui.QStandardItemModel()
        self.modelCAN.setHorizontalHeaderLabels(headerCANh)
        self.modelCAN.setVerticalHeaderLabels(headerCANv)
        rowCount, colCount = self.modelCAN.rowCount(), self.modelCAN.columnCount()
        for row in range(rowCount):
            for col in range(colCount -1):
                self.modelCAN.setItem(row, col, QtGui.QStandardItem('0xXX'))
            self.modelCAN.setItem(row, colCount - 1, QtGui.QStandardItem('YYYY-mm-dd HH:MM:SS'))
        self.tableCAN.setModel(self.modelCAN)
        self.tableCAN.horizontalHeader().setStretchLastSection(True)
        self.tableCAN.horizontalHeader().resizeSections(3)
    
    def tableCANcom(self, msg, *args, **kwargs):
        #echoclient
        id = msg[1]
        data = msg[2:] + msg[0]
        if id in headerCANv:
            row = headerCANv.index(id)
            colCount = self.modelCAN.columnCount()
            for col in range(colCount):
                self.modelCAN.setItem(row, col, QtGui.QStandardItem(data[col]))

    def tableCANall(self, *args, **kwargs):
        query = QtSql.QSqlQuery()
        result = QtSql.QSqlResult()
        colCount = self.modelCAN.columnCount()
        for id in headerCANv:
            row = headerCANv.index(id)
            #query
            for col in range(colCount):
                self.modelCAN.setItem(row, col, QtGui.QStandardItem(data[col]))

    def new(self, *args, **kwargs):
        text, ok = QtGui.QInputDialog.getText(self, 'New Database File', 'Enter Database Name:')
        if ok:
            if not path.exists(text + '.db'):
                if self.db is not None:
                    self.db.close()
                self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
                self.dbname = text
                self.db.setDatabaseName(self.dbname + '.db')
                print self.dbname
                if not self.db.open():
                    QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"), QtGui.qApp.tr(errorDBopen), QtGui.QMessageBox.Cancel)
                    return
                self.connectdb = True
                query = QtSql.QSqlQuery()
                query.exec_("create table candata(date text primary key, id text, b0 text, b1 text, b2 text, b3 text, b4 text, b5 text, b6 text, b7 text)")
                print query.lastQuery()
                for id in headerCANv:
                    query.exec_("insert into candata values('1776-07-04 00:00:0" + str(headerCANv.index(id)) + "', '" + id+ "', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00')")
                    print query.lastQuery()
            else:
                QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot create database"), QtGui.qApp.tr(errorDBexist), QtGui.QMessageBox.Cancel)
    
    def open(self, *args, **kwargs):
        self.dbname = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Database files (*.db)"))
        if self.dbname is not None:
            self.dbname = path.basename(self.dbname)[:-3]
            if self.db is not None:
                self.db.close()
            self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.dbname + '.db')
            print self.dbname
            if not self.db.open():
                QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"), QtGui.qApp.tr(errorDBopen), QtGui.QMessageBox.Cancel)
                return
            self.connectdb = True
            #self.connect()
        #self.tableCANcom(['0x0202', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', 'today'])
    
    def close(self, *args, **kwargs):
        if self.db is not None:
            self.db.close()
        self.db = None
        self.dbname = ''
        self.tableCellinit()
        self.tableTempinit()
        self.tableModinit()
        self.tableCANinit()

    def connect(self, *args, **kwargs):
        with closing(socket.socket()) as s:
            self.HOST = socket.gethostname()
            self.PORT = portNumber
            print "0\n"
            s.bind((self.HOST, self.PORT))
            s.listen(5)
            conn, addr = s.accept()
            with closing(conn):
                print 'Connected by', addr
                while True:
                    data = conn.recv(1024)
                    if data:
                        print data
                        self.tableCANcom(data.split())
                    conn.sendall(data)
                    if data:
                        return

    def closeEvent(self, event, *args, **kwargs):
        if self.db is not None:
            self.db.close()
        sys.exit(0)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())