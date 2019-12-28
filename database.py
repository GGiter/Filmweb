from PyQt5 import QtSql, QtGui 
from PyQt5.QtWidgets import QApplication , QWidget , QMessageBox , qApp
import os
from movie import Movie
from user import User

class Database:
   def __init__(self, name):
      if self.createDB(name):
         self.insertInitialData()

   def createDB(self,database_name):
      self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
      self.db.setDatabaseName(os.path.dirname(os.path.realpath(__file__)) + '/' + database_name)
      
      if not self.db.open():
         QMessageBox.critical(None, qApp.tr("Cannot open database"),
            qApp.tr("Unable to establish a database connection.\n"
               "This example needs SQLite support. Please read "
               "the Qt SQL driver documentation for information "
               "how to build it.\n\n" "Click Cancel to exit."),
            QMessageBox.Cancel)
            
         return False
         
      query = QtSql.QSqlQuery()
      
      query.exec_("CREATE TABLE movies(id INTEGER PRIMARY KEY AUTOINCREMENT , "
         "title varchar(20), director varchar(20) ,description varchar(20))")
         
      query.exec_("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, "
         "login varchar(20), email varchar(20), password varchar(20))")

      query.exec_("CREATE TABLE reviews(player_id INTEGER, "
         "movie_id INTEGER, score INTEGER)")


      return True

   def registerUser(self,login,email,password):
      query = QtSql.QSqlQuery()

      query.exec_(f"INSERT INTO user (login,email,password) VALUES ('{login}', '{email}' ,'{password}')")

      return User(login,email,password)


   def loginUser(self,login,password):
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM user WHERE login = '{login}'")
      query.next()

      if query.record().value("password") != password:
         return None

      return User(login,query.record().value("email"),password)

   
   def getMovies(self):
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM movies")
      movies = []
      while query.next():
         movies.append(Movie(query.record().value("title"),query.record().value("director")))
      
      return movies

   def insertInitialData(self):
      query = QtSql.QSqlQuery()
         
      query.exec_("INSERT INTO movies (id,title,director,description) VALUES (1,'Show', 'Alfred','Lorem lorem')")

      query.exec_("INSERT INTO user (id,login,email,password) VALUES (1,'Bob', 'ross@net.com' ,'Ross')")
