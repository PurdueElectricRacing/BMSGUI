# https://www.tutorialspoint.com/pyqt/pyqt_database_handling.htm
import sys
from PyQt4 import QtCore, QtGui, QtSql

def initializeModel(model):
   model.setTable('sportsmen')
   model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
   model.select()
   model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
   model.setHeaderData(1, QtCore.Qt.Horizontal, "First name")
   model.setHeaderData(2, QtCore.Qt.Horizontal, "Last name")
def createView(title, model):
   view = QtGui.QTableView()
   view.setModel(model)
   view.setWindowTitle(title)
   return view
def addrow():
   print model.rowCount()
   ret = model.insertRows(model.rowCount(), 1)
   print ret
def findrow(i):
   delrow = i.row()
def createDB():
   db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
   db.setDatabaseName('sports.db')
   if not db.open():
      QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
         QtGui.qApp.tr("Unable to establish a database connection.\n"
            "This example needs SQLite support. Please read "
            "the Qt SQL driver documentation for information "
            "how to build it.\n\n" "Click Cancel to exit."),
         QtGui.QMessageBox.Cancel)
      return False
   query = QtSql.QSqlQuery()
   query.exec_("create table sportsmen(id int primary key, "
      "firstname varchar(20), lastname varchar(20))")
   query.exec_("insert into sportsmen values(101, 'Roger', 'Federer')")
   query.exec_("insert into sportsmen values(102, 'Christiano', 'Ronaldo')")
   query.exec_("insert into sportsmen values(103, 'Ussain', 'Bolt')")
   query.exec_("insert into sportsmen values(104, 'Sachin', 'Tendulkar')")
   query.exec_("insert into sportsmen values(105, 'x', 'x')")
   return True
if __name__ == '__main__':

   app = QtGui.QApplication(sys.argv)
   createDB()
   db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
   db.setDatabaseName('sports.db')
   model = QtSql.QSqlTableModel()
   delrow = -1
   initializeModel(model)
   view1 = createView("Table Model (View 1)", model)
   view1.clicked.connect(findrow)
   dlg = QtGui.QDialog()
   layout = QtGui.QVBoxLayout()
   layout.addWidget(view1)
   button = QtGui.QPushButton("Add a row")
   button.clicked.connect(addrow)
   layout.addWidget(button)
   btn1 = QtGui.QPushButton("del a row")
   btn1.clicked.connect(lambda: model.removeRow(view1.currentIndex().row()))
   layout.addWidget(btn1)
   dlg.setLayout(layout)
   dlg.setWindowTitle("Database Demo")
   dlg.show()
   sys.exit(app.exec_())

