from PyQt5 import QtSql, QtGui 
from PyQt5.QtWidgets import QApplication , QWidget , QMessageBox , qApp
import os

def createDB(database_name):
   db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
   db.setDatabaseName(os.path.dirname(os.path.realpath(__file__)) + '/' + database_name)
	
   if not db.open():
      QMessageBox.critical(None, qApp.tr("Cannot open database"),
         qApp.tr("Unable to establish a database connection.\n"
            "This example needs SQLite support. Please read "
            "the Qt SQL driver documentation for information "
            "how to build it.\n\n" "Click Cancel to exit."),
         QMessageBox.Cancel)
			
      return False
		
   query = QtSql.QSqlQuery()
	
   query.exec_("create table movies(id int primary key, "
      "title varchar(20), director varchar(20))")
		
   query.exec_("insert into movies values(101, 'Test', 'Alfred')")

   query.exec_("create table user(id int primary key, "
      "nick varchar(20), email varchar(20))")

   query.exec_("insert into movies values(101, 'Bob', 'ross@net.com')")

   return True
	
if __name__ == '__main__':
   import sys
	
   app = QApplication(sys.argv)
   createDB('filmweb.db')