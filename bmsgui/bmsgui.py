import design
import socket
import sys
import time
from contextlib import closing
from PyQt4 import QtCore, QtGui, QtSql

class MyApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        design.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.actionConnect.triggered.connect(self.connect)

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