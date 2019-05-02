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
        self.connectdb = True
        self.logcounter = 0
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
        self.tableOcvinit()
        self.tableOhminit()
        self.tableModinit()
        self.tableCANinit()
        self.DBinit()
        self.tableCellall()
        self.tableTempall()
        self.tableOcvall()
        self.tableOhmall()
        self.tableModall()
        self.tableCANall()

        self.actionQuit.triggered.connect(self.closeEvent)

        self.pushButtonLog.setVisible(False)
        self.pushButtonDel.setVisible(False)
        self.pushButtonLog.clicked.connect(self.log)
        self.pushButtonDel.clicked.connect(self.delete)
        self.pushButtonLive.clicked.connect(self.live)
        self.pushButtonStop.clicked.connect(self.stop)
        self.pushButtonSet.clicked.connect(self.param)
        
        self.threadCAN = threading.Thread(target=self.threadCANrun)
        self.threadCAN.start()
        if DEBUG:
            state = IDLE
            self.connectdb = True
            self.labelState.setText(labelStates[state])
            self.pushButtonLog.setEnabled(self.connectdb)
            self.pushButtonDel.setEnabled(self.connectdb)
            self.pushButtonLive.setEnabled(self.connectdb)
            self.pushButtonStop.setEnabled(not self.connectdb)

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
        self.tableCell.resizeRowsToContents()

    def tableCellall(self, *args, **kwargs):
        #query = QtSql.QSqlQuery()
        colCount = self.modelCAN.columnCount()
        for id in range(headerCellv):
            row = id
            #query.exec_("select v, date from voltage where id = '" + str(id) +
            #"' order by date desc")
            if PRINT:
                pass #print #query.lastQuery()
            #query.first()
                                #self.modelCell.setItem(row, 0,
                                #QtGui.QStandardItem(str(#query.value(0).toString())))
                                #self.modelCell.setItem(row, 1,
                                #QtGui.QStandardItem(str(#query.value(1).toString())))
    
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
        self.tableTemp.resizeRowsToContents()
    
    def tableTempall(self, *args, **kwargs):
        #query = QtSql.QSqlQuery()
        colCount = self.modelTemp.columnCount()
        for id in range(headerTempv):
            row = id
            #query.exec_("select c, date from temperature where id = '" +
            #str(id) + "' order by date desc")
            if PRINT:
                pass #print #query.lastQuery()
            #query.first()
                                #self.modelTemp.setItem(row, 0,
                                #QtGui.QStandardItem(str(#query.value(0).toString())))
                                #self.modelTemp.setItem(row, 1,
                                #QtGui.QStandardItem(str(#query.value(1).toString())))

    def tableOcvinit(self, *args, **kwargs):
        self.modelOcv = QtGui.QStandardItemModel()
        self.modelOcv.setHorizontalHeaderLabels(headerCellh)
        cellv = []
        for i in range(headerCellv):
            cellv.append('Cell ' + '%02d' % (i,))
        self.modelOcv.setVerticalHeaderLabels(cellv)
        rowCount, colCount = self.modelOcv.rowCount(), self.modelOcv.columnCount()
        for row in range(rowCount):
            for col in range(colCount - 1):
                self.modelOcv.setItem(row, col, QtGui.QStandardItem('-'))
            self.modelOcv.setItem(row, colCount - 1, QtGui.QStandardItem('YYYY-mm-dd HH:MM:SS.MMMMMM'))
        self.tableOcv.setModel(self.modelOcv)
        self.tableOcv.horizontalHeader().setStretchLastSection(True)
        self.tableOcv.horizontalHeader().resizeSections(3)
        self.tableOcv.resizeRowsToContents()

    def tableOcvall(self, *args, **kwargs):
        #query = QtSql.QSqlQuery()
        colCount = self.modelOcv.columnCount()
        for id in range(headerCellv):
            row = id
            #query.exec_("select v, date from ocv where id = '" + str(id) + "'
            #order by date desc")
            if PRINT:
                pass #print #query.lastQuery()
            #query.first()
                                #self.modelOcv.setItem(row, 0,
                                #QtGui.QStandardItem(str(#query.value(0).toString())))
                                #self.modelOcv.setItem(row, 1,
                                #QtGui.QStandardItem(str(#query.value(1).toString())))

    def tableOhminit(self, *args, **kwargs):
        self.modelOhm = QtGui.QStandardItemModel()
        self.modelOhm.setHorizontalHeaderLabels(headerOhmh)
        cellv = []
        for i in range(headerCellv):
            cellv.append('Cell ' + '%02d' % (i,))
        self.modelOhm.setVerticalHeaderLabels(cellv)
        rowCount, colCount = self.modelOhm.rowCount(), self.modelOhm.columnCount()
        for row in range(rowCount):
            for col in range(colCount - 1):
                self.modelOhm.setItem(row, col, QtGui.QStandardItem('-'))
            self.modelOhm.setItem(row, colCount - 1, QtGui.QStandardItem('YYYY-mm-dd HH:MM:SS.MMMMMM'))
        self.tableOhm.setModel(self.modelOhm)
        self.tableOhm.horizontalHeader().setStretchLastSection(True)
        self.tableOhm.horizontalHeader().resizeSections(3)
        self.tableOhm.resizeRowsToContents()

    def tableOhmall(self, *args, **kwargs):
        #query = QtSql.QSqlQuery()
        colCount = self.modelOhm.columnCount()
        for id in range(headerCellv):
            row = id
            #query.exec_("select mohm, date from ir where id = '" + str(id) +
            #"' order by date desc")
            if PRINT:
                pass #print #query.lastQuery()
            #query.first()
                                #self.modelOhm.setItem(row, 0,
                                #QtGui.QStandardItem(str(#query.value(0).toString())))
                                #self.modelOhm.setItem(row, 1,
                                #QtGui.QStandardItem(str(#query.value(1).toString())))

    def tableModinit(self, *args, **kwargs):
        self.modelMod = QtGui.QStandardItemModel()
        self.modelMod.setHorizontalHeaderLabels(headerModh)
        self.modelMod.setVerticalHeaderLabels(headerModv)
        rowCount = self.modelMod.rowCount()
        for row in range(rowCount):
            self.modelMod.setItem(row, 0, QtGui.QStandardItem('-'))
            self.modelMod.setItem(row, 1, QtGui.QStandardItem('YYYY-mm-dd HH:MM:SS.MMMMMM'))
        self.tableMod.setModel(self.modelMod)
        self.tableMod.horizontalHeader().setStretchLastSection(True)
        self.tableMod.horizontalHeader().resizeSections(3)
        self.tableMod.resizeRowsToContents()

    def tableModall(self, *args, **kwargs):
        #query = QtSql.QSqlQuery()
        for id in dbModID:
            row = dbModID.index(id)
            #query.exec_("select v, date from macro where id = '" + str(id) +
            #"' order by date desc")
            if PRINT:
                pass #print #query.lastQuery()
            #query.first()
                                #self.modelMod.setItem(row, 0,
                                #QtGui.QStandardItem(str(#query.value(0).toString())))
                                #self.modelMod.setItem(row, 1,
                                #QtGui.QStandardItem(str(#query.value(1).toString())))

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
        self.tableCAN.resizeRowsToContents()

    def tableCANall(self, *args, **kwargs):
        #query = QtSql.QSqlQuery()
        colCount = self.modelCAN.columnCount()
        for id in headerCANv:
            row = headerCANv.index(id)
            #query.exec_("select len, b0, b1, b2, b3, b4, b5, b6, b7, date from
            #candata where id = '" + id[2:] + "' order by date desc")
            if PRINT:
                pass #print #query.lastQuery()
            #query.first()
                                #for col in range(colCount):
                #self.modelCAN.setItem(row, col,
                                    #QtGui.QStandardItem(str(#query.value(col).toString())))

    def DBinit(self, *args, **kwargs):
        if self.db is not None:
            self.db.close()
        new = 0
        if not path.exists(self.dbname):
            new = 1
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.dbname)
        if PRINT:
            print self.dbname
        if not self.db.open():
            QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"), QtGui.qApp.tr(errorDBopen), QtGui.QMessageBox.Cancel)
            self.db = None
            return
        if new:
            #query = QtSql.QSqlQuery()
            #query.exec_("create table candata(date text primary key, id text,
            #len text, b0 text, b1 text, b2 text, b3 text, b4 text, b5 text, b6
            #text, b7 text)")
            if PRINT:
                pass #print #query.lastQuery()
            #query.exec_("create table voltage(date text primary key, id text,
                                #v text)")
            if PRINT:
                pass #print #query.lastQuery()
            #query.exec_("create table temperature(date text primary key, id
                                #text, c text)")
            if PRINT:
                pass #print #query.lastQuery()
            #query.exec_("create table ocv(date text primary key, id text, v
                                #text)")
            if PRINT:
                pass #print #query.lastQuery()
            #query.exec_("create table ir(date text primary key, id text, mohm
                                #text)")
            if PRINT:
                pass #print #query.lastQuery()
            #query.exec_("create table macro(date text primary key, id text, v
                                #text)")
            if PRINT:
                pass #print #query.lastQuery()
            for id in headerCANv:
                #query.exec_("insert into candata values('1776-07-04 00:00:0" +
                #str(headerCANv.index(id)) + ".000000', '" + id[2:] + "', '8',
                #'0xFF', '0xFF', '0xFF', '0xFF', '0xFF', '0xFF', '0xFF',
                #'0xFF')")
                if PRINT:
                    pass #print #query.lastQuery()
            for id in range(headerCellv):
                #query.exec_("insert into voltage values('1776-07-04 00:00:" +
                #"%02d" % id + ".000000', '" + str(id) + "', '0xFF')")
                if PRINT:
                    pass #print #query.lastQuery()
            for id in range(headerTempv):
                #query.exec_("insert into temperature values('1776-07-04
                #00:00:" + "%02d" % id + ".000000', '" + str(id) + "',
                #'0xFF')")
                if PRINT:
                    pass #print #query.lastQuery()
            for id in range(headerCellv):
                #query.exec_("insert into ocv values('1776-07-04 00:00:" +
                #"%02d" % id + ".000000', '" + str(id) + "', '0xFF')")
                if PRINT:
                    pass #print #query.lastQuery()
            for id in range(headerCellv):
                #query.exec_("insert into ir values('1776-07-04 00:00:" +
                #"%02d" % id + ".000000', '" + str(id) + "', '0xFF')")
                if PRINT:
                    pass #print #query.lastQuery()
            for id in dbModID:
                #query.exec_("insert into macro values('1776-07-04 00:00:" +
                #str(dbModID.index(id)) + ".000000', '" + id + "', '0xFF')")
                if PRINT:
                    pass #print #query.lastQuery()
        self.connectdb = True

    def log(self, *args, **kwargs):
        global state, queue
        msg = 'T62080100000000000000\r' # 0:start
        if not DEBUG:
            ser.write(msg)
        if PRINT:
            print msg
        state = LOG
        queue = []
        self.logname = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '_bms.log'
        self.labelState.setText(labelStates[state])
        self.pushButtonLog.setEnabled(not self.connectdb)
        self.pushButtonDel.setEnabled(not self.connectdb)
        self.pushButtonLive.setEnabled(not self.connectdb)
        self.pushButtonStop.setEnabled(not self.connectdb)

    def delete(self, *args, **kwargs):
        msg = 'T62080200000000000000\r' #1: delete
        if not DEBUG:
            ser.write(msg)
        if PRINT:
            print msg
        
    def live(self, *args, **kwargs):
        global state, queue, ser
        state = LIVE
        queue = []
        self.labelState.setText(labelStates[state])
        self.pushButtonLog.setEnabled(not self.connectdb)
        self.pushButtonDel.setEnabled(not self.connectdb)
        self.pushButtonLive.setEnabled(not self.connectdb)
        self.pushButtonStop.setEnabled(self.connectdb)

    def stop(self, *args, **kwargs):
        global state, ser
        msg = 'T62080300000000000000\r'
        if not DEBUG:
            ser.write("\r\r\r")
            ser.write(msg)
        if PRINT:
            print msg
        state = IDLE
        queue = []
        self.labelState.setText(labelStates[state])
        self.pushButtonLog.setEnabled(self.connectdb)
        self.pushButtonDel.setEnabled(self.connectdb)
        self.pushButtonLive.setEnabled(self.connectdb)
        self.pushButtonStop.setEnabled(not self.connectdb)

    def param(self, *args, **kwargs):
        global ser
        start = "T"
        start += "0" * (3 - len(self.lineEditID.text())) + self.lineEditID.text()
        start += str(self.lineEditLEN.text())
        start += self.lineEditDATA.text()
        if len(self.lineEditDATA.text()) < 2 * int(self.lineEditLEN.text()):
            start += "0" * (2 * int(self.lineEditLEN.text()) - len(self.lineEditDATA.text()))
        #ser.write("\r\r\r")
        ser.write(str(start))
        print start

    def getparam(self, *args, **kwargs):
        if state != 0:
            start = 'T6231'
            for i in range(len(self.lineEditList)):
                m = start + "{0:0{1}x}".format(i, 2)
                if DEBUG:
                    print m
                else:
                    ser.write(m)

    def update():
        print 1
        global state, ser, queue
        if (state == LIVE) and (len(queue) > 0):
            #query = QtSql.QSqlQuery()
            temp = queue
            queue = []
            for entry in temp:
                date = entry[0]
                msg = entry[1]
                m_id = msg[0:3]
                m_len = msg[3:4]
                m_message = msg[4:]
                if m_len == '03':
                    msg = [m_message[0], m_message[1:2]]
                else:
                    msg = [m_message[i:i + 2] for i in range(0, len(m_message), 2)]
                if len(msg) < 8:
                    msg += ['0xXX'] * (8 - len(msg))
                if '0x' + m_id in headerCANv:
                    """
                    #query.prepare("insert into candata (date, id, len, b0, b1, b2, b3, b4, b5, b6, b7) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                    #query.addBindValue(date)
                    #query.addBindValue(m_id)
                    #query.addBindValue(m_len)
                    #query.addBindValue('0x' + msg[0])
                    #query.addBindValue('0x' + msg[1])
                    #query.addBindValue('0x' + msg[2])
                    #query.addBindValue('0x' + msg[3])
                    #query.addBindValue('0x' + msg[4])
                    #query.addBindValue('0x' + msg[5])
                    #query.addBindValue('0x' + msg[6])
                    #query.addBindValue('0x' + msg[7])
                    #query.exec_()
                    """
                # immediate write to modelCAN
                
                    row = headerCANv.index('0x' + m_id)
                    self.modelCAN.setItem(row, 9, QtGui.QStandardItem(date))
                    self.modelCAN.setItem(row, 0, QtGui.QStandardItem(m_len))
                    for i in range(1, 9):
                        self.modelCAN.setItem(row, i, QtGui.QStandardItem('0x' + msg[i - 1]))

                if PRINT:
                    print "insert into candata", entry

                # voltage
                if m_id == headerCANv[0][2:]:
                    b0 = int('0x' + msg[0], 0)
                    b1 = int('0x' + msg[1], 0)
                    c = b0 * cellsPERslave + b1 * dataPERmsg
                    for f in range(1, 1 + dataPERmsg):
                        d = [date[:-1] + str(f), str(c + f - 1), str(int('0x' + msg[2 * f] + msg[2 * f + 1], 0)*.0001)]
                        
                        #query.prepare("insert into voltage (date, id, v)
                        #values (?, ?, ?)")
                        #query.addBindValue(d[0])
                        #query.addBindValue(d[1])
                        #query.addBindValue(d[2])
                        #query.exec_()
                        
                        # immediate write to modelCell
                        self.modelCell.setItem(int(d[1]), 0, QtGui.QStandardItem(d[2]))
                        self.modelCell.setItem(int(d[1]), 1, QtGui.QStandardItem(d[0]))
                        if PRINT:
                            print "insert into voltage", d
                # temp
                if m_id == headerCANv[1][2:]:
                    b0 = int('0x' + msg[0], 0)
                    b1 = int('0x' + msg[1], 0)
                    c = b0 * (headerTempv / slaveNum) + b1
                    for f in range(1, 1 + min(dataPERmsg, headerTempv / slaveNum)):
                        d = [date[:-1] + str(f), str(c + f - 1), str(int('0x' + msg[2 * f] + msg[2 * f + 1], 0)*0.1)]
                        #query.prepare("insert into temperature (date, id,
                        #c) values (?, ?, ?)")
                        #query.addBindValue(d[0])
                        #query.addBindValue(d[1])
                        #query.addBindValue(d[2])
                        #query.exec_()

                        # immediate write to modelTemp
                        self.modelTemp.setItem(int(d[1]), 0, QtGui.QStandardItem(d[2]))
                        self.modelTemp.setItem(int(d[1]), 1, QtGui.QStandardItem(d[0]))

                        if PRINT:
                            print "insert into temp", d
                # ocv
                if m_id == headerCANv[2][2:]:
                    b0 = int('0x' + msg[0], 0)
                    b1 = int('0x' + msg[1], 0)
                    c = b0 * cellsPERslave + b1 * dataPERmsg
                    for f in range(1, 1 + dataPERmsg):
                        d = [date[:-1] + str(f), str(c + f - 1), str(int('0x' + msg[2 * f] + msg[2 * f + 1], 0)*.0001)]
                        #query.prepare("insert into ocv (date, id, v)
                        #values (?, ?, ?)")
                        #query.addBindValue(d[0])
                        #query.addBindValue(d[1])
                        #query.addBindValue(d[2])
                        #query.exec_()

                        # immediate write to modelOcv
                        self.modelOcv.setItem(int(d[1]), 0, QtGui.QStandardItem(d[2]))
                        self.modelOcv.setItem(int(d[1]), 1, QtGui.QStandardItem(d[0]))

                        if PRINT:
                            print "insert into ocv", d
                # ohm
                if m_id == headerCANv[3][2:]:
                    b0 = int('0x' + msg[0], 0)
                    b1 = int('0x' + msg[1], 0)
                    c = b0 * cellsPERslave + b1 * dataPERmsg
                    for f in range(1, 1 + dataPERmsg):
                        d = [date[:-1] + str(f), str(c + f - 1), str(int('0x' + msg[2 * f] + msg[2 * f + 1], 0)*0.001)]
                        #query.prepare("insert into ir (date, id, mohm)
                        #values (?, ?, ?)")
                        #query.addBindValue(d[0])
                        #query.addBindValue(d[1])
                        #query.addBindValue(d[2])
                        #query.exec_()

                        # immediate write to modelOhm
                        self.modelOhm.setItem(int(d[1]), 0, QtGui.QStandardItem(d[2]))
                        self.modelOhm.setItem(int(d[1]), 1, QtGui.QStandardItem(d[0]))

                        if PRINT:
                            print "insert into ir", d
                # mod
                if m_id == headerCANv[5][2:]:
                    soc = int('0x' + msg[0], 0)
                    pvol = int('0x' + msg[1] + msg[2] + msg[3], 0)
                    pcur = int('0x' + msg[4] + msg[5], 0)
                    g = [soc, pvol, pcur]
                    for f in range(3):
                        d = [date[:-1] + str(f), dbModID[f], g[f]]
                        #query.prepare("insert into macro (date, id, v)
                        #values (?, ?, ?)")
                        #query.addBindValue(d[0])
                        #query.addBindValue(d[1])
                        #query.addBindValue(d[2])
                        #query.exec_()
                        if f == 0:
                            d[2] = str(d[2]*0.5) + "%"
                        elif f == 1:
                            d[2] = d[2]*.0001
                        elif f == 2:
                            d[2] = d[2]*0.1
                        # immediate write to modelMod
                        self.modelMod.setItem(dbModID.index(d[1]), 0, QtGui.QStandardItem(str(d[2])))
                        self.modelMod.setItem(dbModID.index(d[1]), 1, QtGui.QStandardItem(d[0]))

                        if PRINT:
                            print "insert into macro", d
                # ack
                if m_id == headerCANv[7][2:]:
                    # might not need to set enable
                    #self.pushButtonSet.setEnabled(True)
                    pass

                # param
                if m_id == headerCANv[8][2:]:
                    self.lineEditList[int(msg[0])].setText(str(int(msg[1], 16)))
    def threadCANrun(self, *args, **kwargs):
        def uupdate():
            global state, ser, queue
            if (state == LIVE) and (len(queue) > 0):
                #query = QtSql.QSqlQuery()
                temp = queue
                queue = []
                for entry in temp:
                    date = entry[0]
                    msg = entry[1]
                    m_id = msg[0:3]
                    m_len = msg[3:4]
                    m_message = msg[4:]
                    if m_len == '03':
                        msg = [m_message[0], m_message[1:2]]
                    else:
                        msg = [m_message[i:i + 2] for i in range(0, len(m_message), 2)]
                    if len(msg) < 8:
                        msg += ['0xXX'] * (8 - len(msg))
                    if '0x' + m_id in headerCANv:
                        """
                        #query.prepare("insert into candata (date, id, len, b0, b1, b2, b3, b4, b5, b6, b7) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                        #query.addBindValue(date)
                        #query.addBindValue(m_id)
                        #query.addBindValue(m_len)
                        #query.addBindValue('0x' + msg[0])
                        #query.addBindValue('0x' + msg[1])
                        #query.addBindValue('0x' + msg[2])
                        #query.addBindValue('0x' + msg[3])
                        #query.addBindValue('0x' + msg[4])
                        #query.addBindValue('0x' + msg[5])
                        #query.addBindValue('0x' + msg[6])
                        #query.addBindValue('0x' + msg[7])
                        #query.exec_()
                        """
                    # immediate write to modelCAN
                
                        row = headerCANv.index('0x' + m_id)
                        self.modelCAN.setItem(row, 9, QtGui.QStandardItem(date))
                        self.modelCAN.setItem(row, 0, QtGui.QStandardItem(m_len))
                        for i in range(1, 9):
                            self.modelCAN.setItem(row, i, QtGui.QStandardItem('0x' + msg[i - 1]))

                    if PRINT:
                        print "insert into candata", entry

                    # voltage
                    if m_id == headerCANv[0][2:]:
                        b0 = int('0x' + msg[0], 0)
                        b1 = int('0x' + msg[1], 0)
                        c = b0 * cellsPERslave + b1 * dataPERmsg
                        for f in range(1, 1 + dataPERmsg):
                            d = [date[:-1] + str(f), str(c + f - 1), str(int('0x' + msg[2 * f] + msg[2 * f + 1], 0)*.0001)]
                        
                            #query.prepare("insert into voltage (date, id, v)
                            #values (?, ?, ?)")
                            #query.addBindValue(d[0])
                            #query.addBindValue(d[1])
                            #query.addBindValue(d[2])
                            #query.exec_()
                        
                            # immediate write to modelCell
                            self.modelCell.setItem(int(d[1]), 0, QtGui.QStandardItem(d[2]))
                            self.modelCell.setItem(int(d[1]), 1, QtGui.QStandardItem(d[0]))
                            if PRINT:
                                print "insert into voltage", d
                    # temp
                    if m_id == headerCANv[1][2:]:
                        b0 = int('0x' + msg[0], 0)
                        b1 = int('0x' + msg[1], 0)
                        c = b0 * (headerTempv / slaveNum) + b1
                        for f in range(1, 1 + min(dataPERmsg, headerTempv / slaveNum)):
                            d = [date[:-1] + str(f), str(c + f - 1), str(int('0x' + msg[2 * f] + msg[2 * f + 1], 0)*0.1)]
                            #query.prepare("insert into temperature (date, id,
                            #c) values (?, ?, ?)")
                            #query.addBindValue(d[0])
                            #query.addBindValue(d[1])
                            #query.addBindValue(d[2])
                            #query.exec_()

                            # immediate write to modelTemp
                            self.modelTemp.setItem(int(d[1]), 0, QtGui.QStandardItem(d[2]))
                            self.modelTemp.setItem(int(d[1]), 1, QtGui.QStandardItem(d[0]))

                            if PRINT:
                                print "insert into temp", d
                    # ocv
                    if m_id == headerCANv[2][2:]:
                        b0 = int('0x' + msg[0], 0)
                        b1 = int('0x' + msg[1], 0)
                        c = b0 * cellsPERslave + b1 * dataPERmsg
                        for f in range(1, 1 + dataPERmsg):
                            d = [date[:-1] + str(f), str(c + f - 1), str(int('0x' + msg[2 * f] + msg[2 * f + 1], 0)*.0001)]
                            #query.prepare("insert into ocv (date, id, v)
                            #values (?, ?, ?)")
                            #query.addBindValue(d[0])
                            #query.addBindValue(d[1])
                            #query.addBindValue(d[2])
                            #query.exec_()

                            # immediate write to modelOcv
                            self.modelOcv.setItem(int(d[1]), 0, QtGui.QStandardItem(d[2]))
                            self.modelOcv.setItem(int(d[1]), 1, QtGui.QStandardItem(d[0]))

                            if PRINT:
                                print "insert into ocv", d
                    # ohm
                    if m_id == headerCANv[3][2:]:
                        b0 = int('0x' + msg[0], 0)
                        b1 = int('0x' + msg[1], 0)
                        c = b0 * cellsPERslave + b1 * dataPERmsg
                        for f in range(1, 1 + dataPERmsg):
                            d = [date[:-1] + str(f), str(c + f - 1), str(int('0x' + msg[2 * f] + msg[2 * f + 1], 0)*0.001)]
                            #query.prepare("insert into ir (date, id, mohm)
                            #values (?, ?, ?)")
                            #query.addBindValue(d[0])
                            #query.addBindValue(d[1])
                            #query.addBindValue(d[2])
                            #query.exec_()

                            # immediate write to modelOhm
                            self.modelOhm.setItem(int(d[1]), 0, QtGui.QStandardItem(d[2]))
                            self.modelOhm.setItem(int(d[1]), 1, QtGui.QStandardItem(d[0]))

                            if PRINT:
                                print "insert into ir", d
                    # mod
                    if m_id == headerCANv[5][2:]:
                        soc = int('0x' + msg[0], 0)
                        pvol = int('0x' + msg[1] + msg[2] + msg[3], 0)
                        pcur = int('0x' + msg[4] + msg[5], 0)
                        g = [soc, pvol, pcur]
                        for f in range(3):
                            d = [date[:-1] + str(f), dbModID[f], g[f]]
                            #query.prepare("insert into macro (date, id, v)
                            #values (?, ?, ?)")
                            #query.addBindValue(d[0])
                            #query.addBindValue(d[1])
                            #query.addBindValue(d[2])
                            #query.exec_()
                            if f == 0:
                                d[2] = str(d[2] * 0.5) + "%"
                            elif f == 1:
                                d[2] = d[2] * .0001
                            elif f == 2:
                                d[2] = d[2] * 0.1
                            # immediate write to modelMod
                            self.modelMod.setItem(dbModID.index(d[1]), 0, QtGui.QStandardItem(str(d[2])))
                            self.modelMod.setItem(dbModID.index(d[1]), 1, QtGui.QStandardItem(d[0]))

                            if PRINT:
                                print "insert into macro", d
                    # ack
                    if m_id == headerCANv[7][2:]:
                        # might not need to set enable
                        #self.pushButtonSet.setEnabled(True)
                        pass

                    # param
                    #if m_id == headerCANv[8][2:]:
                    #    self.lineEditList[int(msg[0])].setText(str(int(msg[1],
                    #    16)))
        global state, ser, queue
        i = 0
        if DEBUG:
            #with open('test0hex.txt') as f:
            #    test0hex = f.read().split('\n')
            #test0hexlen = len(test0hex)
            c = 0
            #print 'here'
            #print test0hexlen
        while(1):
            if state == CLOSE:
                return
            try:
                if state == CLOSE:
                    return
                ser = serial.Serial('COM3', baudrate=5000000, timeout=None)
                ser.write("\r\r\r")
                ser.write('S6\r')   # CAN Baudrate set to 500k
                ser.write('O\r')    # Open CANdapter
                if (state == DISCONNECT):# and self.connectdb:
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
                    if (state > IDLE):#if (in_wait > 0) and (state > IDLE):
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
                        except Exception as e:
                            pass
                    #time.sleep(0.1)
                    if len(queue) > 5:
                        uupdate()

            except Exception as e:
                print e
                # print 'len(queue): ' + str(len(queue))
                if DEBUG:
                    if state == LIVE:
                        if 0 <= (i % 13) <= 2:
                            slaveid = hex(random.randint(0, slaveNum - 1))[2:]
                            if len(slaveid) == 1:
                                slaveid = '0' + slaveid
                            row = hex(random.randint(0, cellsPERslave / dataPERmsg - 1))[2:]
                            if len(row) == 1:
                                row = '0' + row
                            queue.append([str(datetime.datetime.now()), '6058' + slaveid + row + '%012d' % (random.randint(0, 1000000000000))])
                        elif 3 <= (i % 13) <= 4:
                            slaveid = hex(random.randint(0, slaveNum - 1))[2:]
                            if len(slaveid) == 1:
                                slaveid = '0' + slaveid
                            row = '0'#hex(random.randint(0, headerTempv / slaveNum - 1))[2:]
                            if len(row) == 1:
                                row = '0' + row
                            queue.append([str(datetime.datetime.now()), '6068' + slaveid + row + '%012d' % (random.randint(0, 1000000000000))])
                        elif 5 <= (i % 13) <= 7:
                            slaveid = hex(random.randint(0, slaveNum - 1))[2:]
                            if len(slaveid) == 1:
                                slaveid = '0' + slaveid
                            row = hex(random.randint(0, cellsPERslave / dataPERmsg - 1))[2:]
                            if len(row) == 1:
                                row = '0' + row
                            queue.append([str(datetime.datetime.now()), '6078' + slaveid + row + '%012d' % (random.randint(0, 1000000000000))])
                        elif 8 <= (i % 13) <= 10:
                            slaveid = hex(random.randint(0, slaveNum - 1))[2:]
                            if len(slaveid) == 1:
                                slaveid = '0' + slaveid
                            row = hex(random.randint(0, cellsPERslave / dataPERmsg - 1))[2:]
                            if len(row) == 1:
                                row = '0' + row
                            queue.append([str(datetime.datetime.now()), '6088' + slaveid + row + '%012d' % (random.randint(0, 1000000000000))])
                        elif 11 == (i % 13):
                            queue.append([str(datetime.datetime.now()), '60A8' + '%016d' % (random.randint(0, 10000000000000000))])
                        else:
                            queue.append([str(datetime.datetime.now()), '60D3' + '0000' + '%02d' % (random.randint(0, 100))])
                    """if state == LOG:
                        if c == 0:
                            queue.append([str(datetime.datetime.now()), '60C1' + '01'])
                        if c < test0hexlen:
                            queue.append(['0', test0hex[c]])
                            c += 1
                        else:
                            queue.append([str(datetime.datetime.now()), '60C1' + '02'])
                            c = 0 # demo only works with one log
                            time.sleep(0.5)"""
                    uupdate()
                i += 1
                time.sleep(0.2)
                #queue.append([str(datetime.datetime.now()), '60C8' +
                #'0200000000000000'])
                if state == CLOSE:
                    return

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