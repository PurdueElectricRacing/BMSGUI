import datetime
import design
import random
import serial
import socket
import sys
import threading
import time
from constants import *
from contextlib import closing
from os import path
from PyQt4 import QtCore, QtGui, QtSql

state = DISCONNECT
queue = []
ser = None

@fdec(dec)
class MyApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        global state
        QtGui.QMainWindow.__init__(self)
        design.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.connectdb = False
        self.dbname = 'bmsdata.db'
        self.db = None
        self.logname = ''
        self.labelState.setText(labelStates[state])
        self.pushButtonLog.setEnabled(self.connectdb)
        self.pushButtonDel.setEnabled(self.connectdb)
        self.pushButtonLive.setEnabled(self.connectdb)
        self.pushButtonStop.setEnabled(self.connectdb)

        self.tableCellinit()
        self.tableTempinit()
        self.tableModinit()
        self.tableCANinit()
        #tableOcv
        #tableOhm
        self.DBinit()

        self.actionQuit.triggered.connect(self.closeEvent)

        self.pushButtonLog.clicked.connect(self.log)
        self.pushButtonDel.clicked.connect(self.delete)
        self.pushButtonLive.clicked.connect(self.live)
        self.pushButtonStop.clicked.connect(self.stop)
        
        self.threadCAN = threading.Thread(target=self.threadCANrun)
        self.threadCAN.start()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def tableCellinit(self, *args, **kwargs):
        self.modelCell = QtGui.QStandardItemModel()
        self.modelCell.setHorizontalHeaderLabels(headerCellh)
        cellv = []
        for i in range(headerCellv):
            cellv.append('Cell ' + '%02d' % (i,))
        self.modelCell.setVerticalHeaderLabels(cellv)
        rowCount, colCount = self.modelCell.rowCount(), self.modelCell.columnCount()
        for row in range(rowCount):
            for col in range(colCount - 1):
                self.modelCell.setItem(row, col, QtGui.QStandardItem('-'))
            self.modelCell.setItem(row, colCount - 1, QtGui.QStandardItem('YYYY-mm-dd HH:MM:SS.MMMMMM'))
        self.tableCell.setModel(self.modelCell)
        self.tableCell.horizontalHeader().setStretchLastSection(True)
        self.tableCell.horizontalHeader().resizeSections(3)

    def tableCellall(self, *args, **kwargs):
        pass
    
    def tableTempinit(self, *args, **kwargs):
        self.modelTemp = QtGui.QStandardItemModel()
        self.modelTemp.setHorizontalHeaderLabels(headerTemph)
        tempv = []
        for i in range(headerTempv):
            tempv.append('Site ' + '%02d' % (i,))
        self.modelTemp.setVerticalHeaderLabels(tempv)
        rowCount, colCount = self.modelTemp.rowCount(), self.modelTemp.columnCount()
        for row in range(rowCount):
            for col in range(colCount - 1):
                self.modelTemp.setItem(row, col, QtGui.QStandardItem('-'))
            self.modelTemp.setItem(row, colCount - 1, QtGui.QStandardItem('YYYY-mm-dd HH:MM:SS.MMMMMM'))
        self.tableTemp.setModel(self.modelTemp)
        self.tableTemp.horizontalHeader().setStretchLastSection(True)
        self.tableTemp.horizontalHeader().resizeSections(3)
    
    def tableTempall(self, *args, **kwargs):
        pass

    def tableModinit(self, *args, **kwargs):
        #soc soh i with live /ocv mohm seperate
        pass

    def tableCANinit(self, *args, **kwargs):
        self.modelCAN = QtGui.QStandardItemModel()
        self.modelCAN.setHorizontalHeaderLabels(headerCANh)
        self.modelCAN.setVerticalHeaderLabels(headerCANv)
        rowCount, colCount = self.modelCAN.rowCount(), self.modelCAN.columnCount()
        for row in range(rowCount):
            for col in range(colCount - 1):
                if col == 0:
                    self.modelCAN.setItem(row, col, QtGui.QStandardItem('X'))
                else:
                    self.modelCAN.setItem(row, col, QtGui.QStandardItem('0xXX'))
            self.modelCAN.setItem(row, colCount - 1, QtGui.QStandardItem('YYYY-mm-dd HH:MM:SS.MMMMMM'))
        self.tableCAN.setModel(self.modelCAN)
        self.tableCAN.horizontalHeader().setStretchLastSection(True)
        self.tableCAN.horizontalHeader().resizeSections(3)

    def tableCANall(self, *args, **kwargs):
        query = QtSql.QSqlQuery()
        colCount = self.modelCAN.columnCount()
        for id in headerCANv:
            row = headerCANv.index(id)
            query.exec_("select len, b0, b1, b2, b3, b4, b5, b6, b7, date from candata where id = '" + id[2:] + "' order by date desc")
            print query.lastQuery()
            query.first()
            for col in range(colCount):
                self.modelCAN.setItem(row, col, QtGui.QStandardItem(str(query.value(col).toString())))

    def DBinit(self, *args, **kwargs):
        if self.db is not None:
            self.db.close()
        new = 0
        if not path.exists(self.dbname):
            new = 1
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.dbname)
        print self.dbname
        if not self.db.open():
            QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"), QtGui.qApp.tr(errorDBopen), QtGui.QMessageBox.Cancel)
            self.db = None
            return
        if new:
            query = QtSql.QSqlQuery()
            query.exec_("create table candata(date text primary key, id text, len text, b0 text, b1 text, b2 text, b3 text, b4 text, b5 text, b6 text, b7 text)")
            print query.lastQuery()
            query.exec_("create table voltage(date text primary key, id text, v text, mohm text)")
            print query.lastQuery()
            query.exec_("create table temperature(date text primary key, id text, c text)")
            print query.lastQuery()
            for id in headerCANv:
                query.exec_("insert into candata values('1776-07-04 00:00:0" + str(headerCANv.index(id)) + ".000000', '" + id[2:] + "', '0', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00')")
                print query.lastQuery()
        self.connectdb = True
        
        self.tableCANall()

    def log(self, *args, **kwargs):
        global state, queue
        #write
        state = LOG
        queue = []
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
        global state, queue, ser
        #write
        print ser.write('T6103000001\r')
        #print ser.write('T4003000001\r')
        state = LIVE
        queue = []
        self.labelState.setText(labelStates[state])
        self.pushButtonLog.setEnabled(not self.connectdb)
        self.pushButtonDel.setEnabled(not self.connectdb)
        self.pushButtonLive.setEnabled(not self.connectdb)
        self.pushButtonStop.setEnabled(self.connectdb)
        self.tableCANall()

    def stop(self, *args, **kwargs):
        global state, ser
        #write
        ser.write('T6103000000\r')
        state = IDLE
        queue = []
        self.labelState.setText(labelStates[state])
        self.pushButtonLog.setEnabled(self.connectdb)
        self.pushButtonDel.setEnabled(self.connectdb)
        self.pushButtonLive.setEnabled(self.connectdb)
        self.pushButtonStop.setEnabled(not self.connectdb)

    def update(self, *args, **kwargs):
        global state, queue
        if ((state == LIVE) or DEBUG) and (len(queue) > 0):
            query = QtSql.QSqlQuery()
            temp = queue
            queue = []
            for entry in temp:
                date = entry[0]
                msg = entry[1]
                m_id = msg[0:3]
                m_len = msg[3:4]
                m_message = msg[4:]
                msg = [m_message[i:i+2] for i in range(0, len(m_message), 2)]
                query.prepare("insert into candata (date, id, len, b0, b1, b2, b3, b4, b5, b6, b7) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                query.addBindValue(date)
                query.addBindValue(m_id)
                query.addBindValue(m_len)
                query.addBindValue(msg[0])
                query.addBindValue(msg[1])
                query.addBindValue(msg[2])
                query.addBindValue(msg[3])
                query.addBindValue(msg[4])
                query.addBindValue(msg[5])
                query.addBindValue(msg[6])
                query.addBindValue(msg[7])
                query.exec_()
                print "insert into candata", entry
                # voltage
                if m_id == headerCANv[0][2:]:
                    b0 = int('0x' + msg[0], 0)
                    b1 = int('0x' + msg[1], 0)
                    c = b0 * cellsPERslave + b1 * dataPERmsg
                    for f in range(1, 1 + dataPERmsg):
                        query.prepare("insert into voltage (date, id, v, mohm) values (?, ?, ?, ?)")
                        query.addBindValue(date[:-1] + str(f))
                        query.addBindValue(str(int('0x' + msg[2 * f] + msg[2 * f + 1], 0)))
                        query.addBindValue(str(f))
                        query.exec_()
                        print "insert into voltage", entry
            self.tableCellall()
            self.tableTempall()
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

    def threadCANrun(self, *args, **kwargs):
        global state, ser, queue
        i = 0
        while(1):
            if state == CLOSE:
                return
            try:
                if state == CLOSE:
                    return
                ser = serial.Serial('COM3', baudrate=5000000, timeout=None)
                ser.write('S6\r')   # CAN Baudrate set to 500k
                ser.write('O\r')    # Open CANdapter
                if (state == DISCONNECT) and self.connectdb:
                    if state == CLOSE:
                        return
                    state = IDLE
                    self.labelState.setText(labelStates[state])
                    self.pushButtonLog.setEnabled(self.connectdb)
                    self.pushButtonDel.setEnabled(self.connectdb)
                    self.pushButtonLive.setEnabled(self.connectdb)
                    self.pushButtonStop.setEnabled(not self.connectdb)
                while(1):
                    in_wait = ser.in_waiting
                    if state == CLOSE:
                        return
                    if (in_wait > 0) and (state > IDLE):
                        try:
                            message = ser.read_until('\r').replace('\r', '')[1:]
                            m_id = message[0:3]
                            m_len = message[3:4]
                            m_message = message[4:]
                            m_time_stamp = str(datetime.datetime.now())
                            print("id: " + m_id + "\t\tlen: " + m_len + "\t\ttime_stamp: " + m_time_stamp + "\tmsg: " + m_message)
                            if state == LIVE:
                                queue.append([m_time_stamp, message])
                            if state == LOG:
                                queue.append(message)
                        except (serial.serialutil.SerialException):
                            print(str(in_wait) + " !!!!")
            except:
                print i
                if DEBUG:
                    queue.append([str(datetime.datetime.now()), '6058' + '%016d' % (random.randint(0, 10000000000000000))])
                i += 1
                time.sleep(1)
                if state == CLOSE:
                    return
                state = DISCONNECT
                self.labelState.setText(labelStates[state])
                self.pushButtonLog.setEnabled(not self.connectdb)
                self.pushButtonDel.setEnabled(not self.connectdb)
                self.pushButtonLive.setEnabled(not self.connectdb)
                self.pushButtonStop.setEnabled(not self.connectdb)

    def closeEvent(self, event, *args, **kwargs):
        global state
        state = CLOSE
        if self.db is not None:
            self.db.close()
        time.sleep(0.5)
        sys.exit(0)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    #insert into candata values('2019-02-12 17:06:00.000000', '0x605', '8', '9', '2', '3', '4', '5', '6', '7', '8');