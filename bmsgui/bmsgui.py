import design
import socket
import sqlite3
import sys
import time
from contextlib import closing
from PyQt4 import QtCore, QtGui, QtSql
from sqlite3 import Error

class MyApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        design.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.actionNew.triggered.connect(self.createDB)
        #self.actionOpen.triggered.connect()
        self.actionClose.triggered.connect(self.closeEvent)
        #self.actionPreferences.triggered.connect()

    def createDB(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bmsdata.db')
        model = QtSql.QSqlTableModel()
        delrow = -1
        model.setTable('candata')
        model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        model.select()
        model.setHeaderData(0, QtCore.Qt.Horizontal, "CAN ID")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "Data")
        self.tableCAN.setModel(model)
        print self.tableCAN
        print "db"


    def openDB(self):
        print "db"
        if not db.open():
            print "bd"
        query = QtSql.QSqlQuery()
        query.exec_("create table sportsmen(id int primary key, "
            "firstname varchar(20), lastname varchar(20))")
        query.exec_("insert into sportsmen values(101, 'Roger', 'Federer')")
        query.exec_("insert into sportsmen values(102, 'Christiano', 'Ronaldo')")
        query.exec_("insert into sportsmen values(103, 'Ussain', 'Bolt')")
        query.exec_("insert into sportsmen values(104, 'Sachin', 'Tendulkar')")
        query.exec_("insert into sportsmen values(105, 'Saina', 'Nehwal')")
        print "db"

    def connect(self):
        with closing(socket.socket()) as s:
            self.HOST = socket.gethostname()
            self.PORT = 1090
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
                    conn.sendall(data)

    def closeEvent(self, event):
        # closing
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    #time.sleep(5)