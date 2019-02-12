import datetime
import design
import serial
import socket
import sys
from constants import *
from contextlib import closing
from os import path
from PyQt4 import QtCore, QtGui, QtSql

state = DISCONNECT
queue = []

@fdec(dec)
class MyApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        global state
        QtGui.QMainWindow.__init__(self)
        design.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.connectdb = False
        self.dbname = ''
        self.db = None
        self.logname = ''
        self.labelState.setText(labelStates[state])

        self.tableCellinit()
        self.tableTempinit()
        self.tableModinit()
        self.tableCANinit()

        self.actionNew.triggered.connect(self.new)
        self.actionOpen.triggered.connect(self.open)
        self.actionClose.triggered.connect(self.close)
        self.actionClose.setEnabled(self.connectdb)
        self.actionQuit.triggered.connect(self.closeEvent)
        self.actionPreferences.triggered.connect(self.p)

        self.pushButtonLog.clicked.connect(self.log)
        self.pushButtonLog.setEnabled(self.connectdb)
        self.pushButtonDel.clicked.connect(self.delete)
        self.pushButtonDel.setEnabled(self.connectdb)
        self.pushButtonLive.clicked.connect(self.live)
        self.pushButtonLive.setEnabled(self.connectdb)
        self.pushButtonStop.clicked.connect(self.stop)
        self.pushButtonStop.setEnabled(self.connectdb)

        self.threadRead = MyThreadRead()
        self.threadRead.start()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def p(self, *args, **kwargs):
        pass

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
        query = QtSql.QSqlQuery()
        query.exec_("insert into candata values('" + msg[0] + "', '" + msg[1] + "', '" + msg[2] + "', '" + msg[3] + "', '" + msg[4] + "', '" + msg[5] + "', '" + msg[6] + "', '" + msg[7] + "', '" + msg[8] + "')")
        print query.lastQuery()
        id = msg[1]
        data = msg[2:] + [msg[0]]
        if id in headerCANv:
            row = headerCANv.index(id)
            colCount = self.modelCAN.columnCount()
            for col in range(colCount):
                self.modelCAN.setItem(row, col, QtGui.QStandardItem(data[col]))

    def tableCANall(self, *args, **kwargs):
        query = QtSql.QSqlQuery()
        colCount = self.modelCAN.columnCount()
        for id in headerCANv:
            row = headerCANv.index(id)
            query.exec_("select b0, b1, b2, b3, b4, b5, b6, b7, date from candata where id = '" + id + "' order by date desc")
            print query.lastQuery()
            query.first()
            for col in range(colCount):
                self.modelCAN.setItem(row, col, QtGui.QStandardItem(str(query.value(col).toString())))

    def new(self, *args, **kwargs):
        global state
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
                    self.db = None
                    return

                self.connectdb = True
                state = IDLE
                self.actionClose.setEnabled(self.connectdb)
                self.labelState.setText(labelStates[state])
                self.pushButtonLog.setEnabled(self.connectdb)
                self.pushButtonDel.setEnabled(self.connectdb)
                self.pushButtonLive.setEnabled(self.connectdb)
                self.pushButtonStop.setEnabled(not self.connectdb)

                query = QtSql.QSqlQuery()
                query.exec_("create table candata(date text primary key, id text, b0 text, b1 text, b2 text, b3 text, b4 text, b5 text, b6 text, b7 text)")
                print query.lastQuery()
                for id in headerCANv:
                    query.exec_("insert into candata values('1776-07-04 00:00:00" + str(headerCANv.index(id)) + "', '" + id+ "', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00')")
                    print query.lastQuery()
            else:
                QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot create database"), QtGui.qApp.tr(errorDBexist), QtGui.QMessageBox.Cancel)
    
    def open(self, *args, **kwargs):
        global state
        self.dbname = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Database files (*.db)"))
        if self.dbname is not '':
            self.dbname = path.basename(self.dbname)[:-3]
            if self.db is not None:
                self.db.close()
            self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.dbname + '.db')
            print self.dbname
            if not self.db.open():
                QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"), QtGui.qApp.tr(errorDBopen), QtGui.QMessageBox.Cancel)
                self.db = None
                return
            self.tableCANall()

            self.connectdb = True
            state = IDLE
            self.actionClose.setEnabled(self.connectdb)
            self.labelState.setText(labelStates[state])
            self.pushButtonLog.setEnabled(self.connectdb)
            self.pushButtonDel.setEnabled(self.connectdb)
            self.pushButtonLive.setEnabled(self.connectdb)
            self.pushButtonStop.setEnabled(not self.connectdb)
    
    def close(self, *args, **kwargs):
        global state
        if self.db is not None:
            self.db.close()
        self.db = None
        self.connectdb = False
        state = DISCONNECT
        self.dbname = ''
        self.tableCellinit()
        self.tableTempinit()
        self.tableModinit()
        self.tableCANinit()
        self.labelState.setText(labelStates[state])
        self.actionClose.setEnabled(self.connectdb)

    def log(self, *args, **kwargs):
        global state, queue
        #write
        state = LOG
        self.logname = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '_bms.log'
        self.labelState.setText(labelStates[state])
        self.pushButtonLog.setEnabled(not self.connectdb)
        self.pushButtonDel.setEnabled(not self.connectdb)
        self.pushButtonLive.setEnabled(not self.connectdb)
        self.pushButtonStop.setEnabled(not self.connectdb)

    def delete(self, *args, **kwargs):
        #write
        pass

    def live(self, *args, **kwargs):
        global state, queue
        #write
        state = LIVE
        self.labelState.setText(labelStates[state])
        self.pushButtonLog.setEnabled(not self.connectdb)
        self.pushButtonDel.setEnabled(not self.connectdb)
        self.pushButtonLive.setEnabled(not self.connectdb)
        self.pushButtonStop.setEnabled(self.connectdb)
        self.tableCANall()

    def stop(self, *args, **kwargs):
        global state
        #write
        state = IDLE
        self.labelState.setText(labelStates[state])
        self.pushButtonLog.setEnabled(self.connectdb)
        self.pushButtonDel.setEnabled(self.connectdb)
        self.pushButtonLive.setEnabled(self.connectdb)
        self.pushButtonStop.setEnabled(not self.connectdb)

    def update(self, *args, **kwargs):
        global state, queue
        if (state == LIVE) and (len(queue) > 0):
            query = QtSql.QSqlQuery()
            temp = queue
            queue = []
            for entry in temp:
                msg = entry.split(', ')
                query.prepare("insert into candata (date, id, b0, b1, b2, b3, b4, b5, b6, b7) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                query.addBindValue(msg[0])
                query.addBindValue(msg[1])
                query.addBindValue(msg[2])
                query.addBindValue(msg[3])
                query.addBindValue(msg[4])
                query.addBindValue(msg[5])
                query.addBindValue(msg[6])
                query.addBindValue(msg[7])
                query.addBindValue(msg[8])
                query.addBindValue(msg[9])
                query.exec_()
                print "insert into candata", msg
            self.tableCANall()
        elif (state == LOG) and (len(queue) > 0):
            temp = queue
            queue = []
            with open(self.logname, 'a') as f:
                for entry in temp:
                    if entry == 'END':
                        state = IDLE
                        self.labelState.setText(labelStates[state])
                        self.pushButtonLog.setEnabled(self.connectdb)
                        self.pushButtonDel.setEnabled(self.connectdb)
                        self.pushButtonLive.setEnabled(self.connectdb)
                        self.pushButtonStop.setEnabled(not self.connectdb)
                        break
                    else:
                        f.write(entry)

    def write(self, *args, **kwargs):
        HOST = socket.gethostname()
        PORT = portNumber
        with closing(socket.socket()) as s:
            s.connect((self.HOST, self.PORT))
            while True:
                i = raw_input("Message: ")
                s.sendall(i)
                data = s.recv(1024)
                print repr(data)

    def closeEvent(self, event, *args, **kwargs):
        if self.db is not None:
            self.db.close()
        self.threadRead.exit()
        sys.exit(0)

@fdec(dec)
class MyThreadRead(QtCore.QThread):
    def __init__(self, *args, **kwargs):
        return super(MyThreadRead, self).__init__(*args)

    def run(self, *args, **kwargs):
        global state, queue
        ser = serial.Serial('COM3', baudrate=5000000, timeout=None)
        #ser.open()
        print(ser.write('S6\r'))    # CAN Baudrate set to 500k
        print(ser.write('O\r'))     # Open CANdapter
        print 0
        print(ser.write('T352411223344\r'))
        print 1
        while(1):
            in_wait = ser.in_waiting
            if(in_wait > 0):
                try:
                    # Message format
                    # tIIILDDDDDDDDTTTT
                    # III = CAN ID
                    # L = Message Length
                    # D = Message data
                    # T = Timestamp

                    message = ser.read_until('\r').replace('\r', '')[1:]
                    m_id = message[0:3]
                    m_len = message[3:4]
                    m_message = message[4:]
                    m_time_stamp = str(datetime.datetime.now())
                    print("id: " + m_id + "\t\tlen: " + m_len + "\t\ttime_stamp: " + m_time_stamp + "\tmsg: " + m_message)
                except (serial.serialutil.SerialException):
                    print(str(in_wait) + " !!!!")
        while(1):
            with closing(socket.socket()) as s:
                s.bind((socket.gethostname(), portNumber))
                s.listen(5)
                conn, addr = s.accept()
                with closing(conn):
                    print 'MyThreadRead connected by', addr
                    while True:
                        data = conn.recv(1024)
                        if len(data) == 0:
                            print 'MyThreadRead disconnected'
                            break
                        if data:
                            print 'MyThreadRead:', data
                            if state == LIVE:
                                queue.append(data)
                            if state == LOG:
                                queue.append(data)
                        conn.sendall(data)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    #2019-02-02 16:34:00, 0x0202, 19, 11, 12, 13, 14, 15, 16, 17