from data_objects.movie import Movie
from data.database import Database
from random import randrange

emails_prefixs = ["gonzo","bonzo","kapelusz","szalik","zajac","internet"]
emails_suffixs = ["net.com","gmail.com","pw.pl","internet"]
logins = ["gonzo","bonzo","kapelusz","szalik","zajac","internet","marszalek","skyr","ross"] 
passwords = ["rogalik"]


def generate_users(db):
    x = 0 
    while x < len(logins):
      email = ""
      email += emails_prefixs[randrange(len(emails_prefixs))]
      email += "@"
      email += emails_suffixs[randrange(len(emails_suffixs))]
      login = logins[randrange(len(logins))]
      password = passwords[randrange(len(passwords))]
      if db.register_user(login,email,password) is None :
          x += 1


titles = ["Honolulu","Escape","Great Escape","Monkey","Bones"]
directors = ["Andrew Jack","Bob Ross","Hugh Jogh"] 
descriptions = ["Lorem lorem","ipsum ipsum","box"]
durations = [120,140,89]
actors = ["Andrew Jack","Bob Ross","Hugh Jogh"]
genres = ["action","mystery","thriller","comedy"]

def generate_movies(db):
    x = 0 
    while x < len(titles):
        title = titles[randrange(len(titles))]
        director = directors[randrange(len(directors))]
        description = descriptions[randrange(len(descriptions))]
        duration = durations[randrange(len(durations))]
        actor = actors[randrange(len(actors))]
        genre = genres[randrange(len(genres))]
        if db.add_movie(Movie(title,director,description,duration,actor,genre)) is True:
            x += 1



def generate_reviews(db):
    x = 0
    while x < 20:
        user_id = randrange(1,10)
        movie_id = randrange(1,10)
        score = randrange(1,11)
        if db.add_review(user_id,movie_id,score) is True:
            x += 1

if __name__ == '__main__':
  db = Database('filmweb.db')
  generate_users(db)
  generate_movies(db)
  generate_reviews(db)
  
        