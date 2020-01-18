from PyQt5 import QtSql
from PyQt5.QtWidgets import QMessageBox , qApp
from data_objects.movie import Movie
from data_objects.user import User
from data_objects.review import Review
import os

class Database:
   """Class that represents sq lite database.
      @name : path of the database to load or create , path should be relative to script 
      @db : database object
   """
   def __init__(self, name):
      self.name = name
      self.create_database(name)

   def create_database(self,database_name):
      """
      Loads or creates database ,
      adds movies,users,reviews tables to database
      """
      self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
      self.db.setDatabaseName(os.path.dirname(os.path.realpath(__file__)) + '/' + database_name)
      
      if not self.db.open():
         QMessageBox.critical(None, qApp.tr("Cannot open database"),
            qApp.tr("Unable to establish a database connection."),
            QMessageBox.Cancel)
         return False
         
      query = QtSql.QSqlQuery()
      
      query.exec_("CREATE TABLE movies(id INTEGER PRIMARY KEY AUTOINCREMENT , "
         "title varchar(20), director varchar(20) ,description varchar(20),duration INT ,"
         " actors varchar(100) , genre varchar(20), icon_path varchar(100))")
         
      query.exec_("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, "
         "login varchar(20), email varchar(20), password varchar(20), icon_path varchar(100))")

      query.exec_("CREATE TABLE reviews(id INTEGER PRIMARY KEY AUTOINCREMENT,player_id INTEGER, "
         "movie_id INTEGER, score INTEGER)")

      return True

   def get_field_by_id(self,table_name,field_name,id):
      """
      Get field value from database by id 
      """
      return self.get_field_by_parameter(table_name,field_name,"id",id)

   def get_field_by_parameter(self,table_name,field_name,parameter,value):
      """
      Get field value from database by specified parameter
      """
      query = QtSql.QSqlQuery()
      query.exec_(f"SELECT {field_name} FROM {table_name} WHERE {parameter} = '{value}'")
      query.next()

      if query.isValid() is False:
         return None

      return query.value(0)

   def register_user(self,login,email,password):
      """
      Register user if data is valid 
      return None if fails 
      return User object if succeeds
      """
      if (len(email) == 0 or len(login) == 0 or len(password) == 0 
         or self.get_field_by_parameter("users","login","login",login) is not None 
         or self.get_field_by_parameter("users","email","email",email) is not None
         or email.find('@') <= 0 ):      
         return None
      
      query = QtSql.QSqlQuery()

      query.exec_(f"INSERT INTO users (login,email,password,icon_path) "
                  f"VALUES ('{login}', '{email}' ,'{password}','None')")

      return User(login,email,password,query.record().value("icon_path"),query.record().value("id"))


   def login_user(self,login,password):
      """
      Login user if data is valid 
      return None if fails
      return User object if succeeds
      """
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM users WHERE login = '{login}'")

      query.next()

      record = query.record()

      if query.isValid() is False or record.value("password") != password:
         return None

      return User(login,record.value("email"),record.value("icon_path"),password,record.value("id"))

   def get_users(self):
      """
      Get all users from database
      """
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM users")

      users = []
      while query.next():
         record = query.record()
         users.append(User(record.value("login"),record.value("email"),
         record.value("password"),record.value("icon_path"),record.value("id")
         ))
      
      return users
   
   def get_movies(self):
      """
      Get all movies from database
      update avg_rate for each movie
      """
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM movies")

      movies = []
      while query.next():
         record = query.record()
         movie = Movie(record.value("title"),record.value("director"),
         record.value("description"),record.value("duration"),record.value("actors"),record.value("genre"),
         record.value("icon_path"),record.value("id")
         )
         movies.append(movie)
         reviews = self.get_movie_reviews(movie)
         scores = [review.get_score() for review in reviews]
         if len(reviews) > 0 :
            movie.set_avg_rate(int(sum(scores)/len(reviews)),len(reviews))
 
      return movies

   def get_movies_by_parameter(self,parameter,value):
      """
      Get movies if they pass the specified parameter
      """
      query = QtSql.QSqlQuery()

      if parameter is not "actors":
         query.exec_(f"SELECT * FROM movies WHERE {parameter} LIKE '{value}%'")
      else:
         query.exec_(f"SELECT * FROM movies WHERE {parameter} LIKE '%{value}%'")
      movies = []
      while query.next():
         record = query.record()
         movie = Movie(record.value("title"),record.value("director"),
         record.value("description"),record.value("duration"),record.value("actors"),
         record.value("genre"),record.value("icon_path"),record.value("id")
         )
         movies.append(movie)
      return movies

   def get_user_reviews(self,user):
      """
      Get reviews commited by specified user
      """
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM reviews WHERE player_id = {user.get_id()}")
      reviews = []
      while query.next():
         record = query.record()
         reviews.append(Review(record.value("player_id"),record.value("movie_id"),
         record.value("score")
         ))

      return reviews

   def get_movie_reviews(self,movie):
      """
      Get all reviews for specified movie
      """
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM reviews WHERE movie_id = {movie.get_id()}")
      reviews = []
      while query.next():
         record = query.record()
         reviews.append(Review(record.value("player_id"),record.value("movie_id"),
         record.value("score")
         ))

      return reviews

   def add_movie(self,movie):
      """
      Add movie to database if data is valid
      return True if succeeds
      return False if fails
      """
      query = QtSql.QSqlQuery()

      if (self.get_field_by_parameter("movies","title","title",movie.get_title()) is not None
          or len(movie.get_title()) == 0 or len(movie.get_director()) == 0):
         return False

      query.exec_(f"INSERT INTO movies (title,director,description,duration,actors,genre,icon_path)"
      f" VALUES ('{movie.get_title()}', '{movie.get_director()}','{movie.get_description()}',{movie.get_duration()},"
      f"'{movie.get_actors()}','{movie.get_genre()}','{movie.get_icon_path()}')")

      return True


   def rate_movie(self,user,movie,score):
      """
      Add review to database 
      update avg rate for each movie
      """
      self.add_review(user.get_id(),movie.get_id(),score)
 
      #update avg rate for each movie
      reviews = self.get_movie_reviews(movie)
      scores = [review.get_score() for review in reviews]
      if len(reviews) > 0 :
            movie.set_avg_rate(int(sum(scores)/len(reviews)),len(reviews))

   def add_review(self,user_id,movie_id,score):
      """
      Add review to database 
      return True if succeeds
      return False if fails
      """
      if (self.get_field_by_parameter("users","id","id",user_id) is None or
         self.get_field_by_parameter("movies","id","id",movie_id) is None or
         score > 10 or score < 1):
         return False 
      
      query = QtSql.QSqlQuery()

      query.exec_(f"SELECT * FROM reviews WHERE player_id = {user_id} AND movie_id = {movie_id}")

      query.next()

      if query.isValid() is True : 
         query.exec_(f"UPDATE reviews SET score = {score} WHERE player_id = {user_id} AND movie_id = {movie_id}")
      else:
         query.exec_(f"INSERT INTO reviews (player_id,movie_id,score) VALUES ({user_id},{movie_id},{score})")

      return True


   def clear(self):
      """
      Destroy all tables 
      create new empty movies,users,reviews tables
      return True if succeeds 
      return False if fails
      """
      query = QtSql.QSqlQuery()

      query.exec_("DROP TABLE movies")
      query.exec_("DROP TABLE users")
      query.exec_("DROP TABLE reviews")

      return self.create_database(self.name)

      


      
      
