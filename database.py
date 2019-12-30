from PyQt5 import QtSql, QtGui 
from PyQt5.QtWidgets import QApplication , QWidget , QMessageBox , qApp
import os
from movie import Movie
from user import User
from review import Review

class Database:
   def __init__(self, name):
      if self.createDB(name):
         self.insert_initial_data()

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
         "title varchar(20), director varchar(20) ,description varchar(20), actors varchar(100) , genre varchar(20))")
         
      query.exec_("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, "
         "login varchar(20), email varchar(20), password varchar(20))")

      query.exec_("CREATE TABLE reviews(id INTEGER PRIMARY KEY AUTOINCREMENT,player_id INTEGER, "
         "movie_id INTEGER, score INTEGER)")


      return True

   def get_field(self,table_name,field_name,id):
      query = QtSql.QSqlQuery()
      query.exec_(f"SELECT {field_name} FROM {table_name} WHERE id = '{id}'")
      query.next()

      return str(query.value(0))


   def register_user(self,login,email,password):
      query = QtSql.QSqlQuery()

      query.exec_(f"INSERT INTO user (login,email,password) VALUES ('{login}', '{email}' ,'{password}')")

      return User(login,email,password,query.record().value("id"))


   def login_user(self,login,password):
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM user WHERE login = '{login}'")
      query.next()

      if query.record().value("password") != password:
         return None

      return User(login,query.record().value("email"),password,query.record().value("id"))

   def get_users(self):
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM user")
      users = []
      while query.next():
         users.append(User(query.record().value("login"),query.record().value("email"),
         query.record().value("password"),query.record().value("id")
         ))
      
      return users
   
   def get_movies(self):
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM movies")
      movies = []
      while query.next():
         movie = Movie(query.record().value("title"),query.record().value("director"),
         query.record().value("description"),query.record().value("actors"),query.record().value("genre"),query.record().value("id")
         )
         movies.append(movie)
         reviews = self.get_movie_reviews(movie)
         scores = [review.get_score() for review in reviews]
         if len(reviews) > 0 :
            movie.set_avg_rate(int(sum(scores)/len(reviews)),len(reviews))
 
      
      return movies

   def get_user_reviews(self,user):
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM reviews WHERE player_id = {user.get_id()}")
      reviews = []
      while query.next():
         reviews.append(Review(query.record().value("player_id"),query.record().value("movie_id"),
         query.record().value("score")
         ))

      return reviews

   def get_movie_reviews(self,movie):
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM reviews WHERE movie_id = {movie.get_id()}")
      reviews = []
      while query.next():
         reviews.append(Review(query.record().value("player_id"),query.record().value("movie_id"),
         query.record().value("score")
         ))

      return reviews

   def insert_initial_data(self):
      query = QtSql.QSqlQuery()
         
      query.exec_("INSERT INTO movies (id,title,director,description,actors,genre) VALUES (1,'Show', 'Alfred','Lorem lorem','Pip brad','action')")

      query.exec_("INSERT INTO movies (id,title,director,description,actors,genre) VALUES (2,'Escape', 'John','Ipsilum Ipsilum','Bran','mystery')")

      query.exec_("INSERT INTO user (id,login,email,password) VALUES (1,'Bob', 'ross@net.com' ,'Ross')")
      

      query.exec_("INSERT INTO reviews (id,player_id,movie_id,score) VALUES (1,1,1,5)")

   def add_movie(self,movie):
      query = QtSql.QSqlQuery()

      query.exec_(f"INSERT INTO movies (title,director,description,actors,genre) VALUES ('{movie.get_title()}', '{movie.get_director()}','{movie.get_description()}','{movie.get_actors()}','{movie.get_genre()}')")


   def rate_movie(self,user,movie,score):
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM reviews WHERE player_id = {user.get_id()} AND player_id = {movie.get_id()}")

      if query.value(0) is None : 
         query.exec_(f"UPDATE reviews SET score = {score} WHERE player_id = {user.get_id()} AND player_id = {movie.get_id()}")
      else:
         query.exec_(f"INSERT INTO reviews (player_id,movie_id,score) VALUES ({user.get_id()},{movie.get_id()},{score})")

      
      
