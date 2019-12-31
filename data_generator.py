from database import Database
from random import randrange
from data_objects.movie import Movie
emails_prefixs = ["gonzo","bonzo","kapelusz","szalik","zajac","internet"]
emails_suffixs = ["net.com","gmail.com","pw.pl","internet"]
logins = ["gonzo","bonzo","kapelusz","szalik","zajac","internet","marszalek","skyr","ross"] 
passwords = ["rogalik"]


def generate_users(db):
    for x in range(20):
      email = ""
      email += emails_prefixs[randrange(len(emails_prefixs))]
      email += "@"
      email += emails_suffixs[randrange(len(emails_suffixs))]
      login = logins[randrange(len(logins))]
      password = passwords[randrange(len(passwords))]
      db.register_user(login,email,password)


titles = ["Honolulu","Escape","Great Escape","Monkey","Bones"]
directors = ["Andrew Jack","Bob Ross","Hugh Jogh"] 
descriptions = ["Lorem lorem","ipsum ipsum","box"]
durations = [120,140,89]
actors = ["Andrew Jack","Bob Ross","Hugh Jogh"]
genres = ["action","mystery","thriller","comedy"]

def generate_movies(db):
    for x in range(20):
        title = titles[randrange(len(titles))]
        director = directors[randrange(len(directors))]
        description = descriptions[randrange(len(descriptions))]
        duration = durations[randrange(len(durations))]
        actor = actors[randrange(len(actors))]
        genre = genres[randrange(len(genres))]
        db.add_movie(Movie(title,director,description,duration,actor,genre))



def generate_reviews(db):
    for x in range(20):
        user_id = randrange(1,10)
        movie_id = randrange(1,10)
        score = randrange(1,11)
        db.add_review(user_id,movie_id,score)

if __name__ == '__main__':
  db = Database('filmweb.db')
  generate_users(db)
  generate_movies(db)
  generate_reviews(db)
  
        