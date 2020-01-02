from PyQt5 import QtSql, QtGui 
from PyQt5.QtWidgets import QApplication , QWidget , QMessageBox , qApp
import os
from data_objects.movie import Movie
from data_objects.user import User
from data_objects.review import Review

class Database:
   def __init__(self, name):
      self.name = name
      self.createDB(name)

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
         "title varchar(20), director varchar(20) ,description varchar(20),duration INT, actors varchar(100) , genre varchar(20), icon_path varchar(100))")
         
      query.exec_("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, "
         "login varchar(20), email varchar(20), password varchar(20), icon_path varchar(100))")

      query.exec_("CREATE TABLE reviews(id INTEGER PRIMARY KEY AUTOINCREMENT,player_id INTEGER, "
         "movie_id INTEGER, score INTEGER)")
      return True

   def get_field(self,table_name,field_name,id):
      return self.get_field_by_parameter(table_name,field_name,"id",id)

   def get_field_by_parameter(self,table_name,field_name,parameter,value):
      query = QtSql.QSqlQuery()
      query.exec_(f"SELECT {field_name} FROM {table_name} WHERE {parameter} = '{value}'")
      query.next()

      if query.isValid() is False:
         return None

      return str(query.value(0))

   def register_user(self,login,email,password):
      
      if len(email) == 0 or len(login) == 0 or len(password) == 0 or self.get_field_by_parameter("users","login","login",login) is not None or self.get_field_by_parameter("users","email","email",email) is not None:      
         return None
      
      query = QtSql.QSqlQuery()

      query.exec_(f"INSERT INTO users (login,email,password,icon_path) VALUES ('{login}', '{email}' ,'{password}','None')")

      return User(login,email,password,query.record().value("icon_path"),query.record().value("id"))


   def login_user(self,login,password):
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM users WHERE login = '{login}'")
      query.next()

      if query.record().value("password") != password:
         return None

      return User(login,query.record().value("email"),query.record().value("icon_path"),password,query.record().value("id"))

   def get_users(self):
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM users")
      users = []
      while query.next():
         users.append(User(query.record().value("login"),query.record().value("email"),
         query.record().value("password"),query.record().value("icon_path"),query.record().value("id")
         ))
      
      return users
   
   def get_movies(self):
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM movies")
      movies = []
      while query.next():
         movie = Movie(query.record().value("title"),query.record().value("director"),
         query.record().value("description"),query.record().value("duration"),query.record().value("actors"),query.record().value("genre"),query.record().value("icon_path")
         ,query.record().value("id")
         )
         movies.append(movie)
         reviews = self.get_movie_reviews(movie)
         scores = [review.get_score() for review in reviews]
         if len(reviews) > 0 :
            movie.set_avg_rate(int(sum(scores)/len(reviews)),len(reviews))
 
      
      return movies

   def get_movies_by_key(self,key,value):
      query = QtSql.QSqlQuery()

      if key is not "actors":
         query.exec_(f"SELECT * FROM movies WHERE {key} LIKE '{value}%'")
      else:
         query.exec_(f"SELECT * FROM movies WHERE {key} LIKE '%{value}%'")
      movies = []
      while query.next():
         movie = Movie(query.record().value("title"),query.record().value("director"),
         query.record().value("description"),query.record().value("duration"),query.record().value("actors"),query.record().value("genre"),query.record().value("icon_path")
         ,query.record().value("id")
         )
         movies.append(movie)
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

   def add_movie(self,movie):
      query = QtSql.QSqlQuery()

      if self.get_field_by_parameter("movies","title","title",movie.get_title()) is not None or len(movie.get_title()) == 0 or len(movie.get_director()) == 0:
         return False

      query.exec_(f"INSERT INTO movies (title,director,description,duration,actors,genre,icon_path) VALUES ('{movie.get_title()}', '{movie.get_director()}','{movie.get_description()}',{movie.get_duration()},'{movie.get_actors()}','{movie.get_genre()}','{movie.get_icon_path()}')")

      return True


   def rate_movie(self,user,movie,score):
      self.add_review(user.get_id(),movie.get_id(),score)
 
      reviews = self.get_movie_reviews(movie)
      scores = [review.get_score() for review in reviews]
      if len(reviews) > 0 :
            movie.set_avg_rate(int(sum(scores)/len(reviews)),len(reviews))

   def add_review(self,user_id,movie_id,score):
      
      if self.get_field_by_parameter("users","id","id",user_id) is None or self.get_field_by_parameter("movies","id","id",movie_id) is None or score > 10 or score < 1:
         return False 
      
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM reviews WHERE player_id = {user_id} AND player_id = {movie_id}")

      if query.isValid() is True : 
         query.exec_(f"UPDATE reviews SET score = {score} WHERE player_id = {user_id} AND player_id = {movie_id}")
      else:
         query.exec_(f"INSERT INTO reviews (player_id,movie_id,score) VALUES ({user_id},{movie_id},{score})")

      return True


   def clear(self):
      query = QtSql.QSqlQuery()

      query.exec_("DROP TABLE movies")
      query.exec_("DROP TABLE users")
      query.exec_("DROP TABLE reviews")

      self.createDB(self.name)


      
      
