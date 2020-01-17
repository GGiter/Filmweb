from data_objects.movie import Movie
from data.database import Database
from random import randrange

emails_prefixs = ["gonzo","bonzo","kapelusz","szalik","zajac","internet","abattoir"
,"abbadon","slark","renifer"]
emails_suffixs = ["net.com","gmail.com","pw.pl","internet"]
logins = ["gonzo","bonzo","kapelusz","szalik","zajac","internet","marszalek","skyr","ross"
,"Arrosive","Bracteate","Juramentum","Gallivant","Contraband","Trochoid","CshootBlithe"] 
passwords = ["rogalik","renifer","skyrim","kapelusz","wonsz"]


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


titles = ["Honolulu","Escape","Great Escape","Monkey","Bones","Joker","Zootopia","The Jungle Book"
,"Bohemian","Skyfall","Iron man","Minions","Toy Story","Incredibles","Incredibles 2","Jurrasic World","Jurrasic World 2","Rayman"
,"Spectre","Casino Royale","Lampion","Reddit","Bubble","Frozen","Frozen 2","Frozen 3","Incredibles 3"]
directors = ["Andrew Jack","Bob Ross","Hugh Jogh","Tim Burton","Hugh Jackson","Woody Allen","James Cameron"] 
descriptions = ["Sympathetic teacher DCI HANNAH COCKLE is arguing with delightful teacher DR ZACH DONALDSON. HANNAH tries to hug ZACH but he shakes her off."
,"The relaxed life of a woman take a sharp turn as a friendly acquaintance enters her life."
,"The rough life of a woman will be changed completely as a strange woman enters her life."
,"The carefree life of a teenage boy changes in an instant as a strange man enters his life."
,"The calm life of a girl is going the complete opposite way as a lost friend enters her life."
,"The stable life of a girl changes in an instant as a neighbor enters her life."
,"The relaxed life of a teenage boy changes in an instant as a neighbor enters his life."
,"The smooth life of a teenage boy is going the complete opposite way as a stranger enters his life."
,"The secluded life of a woman will be permanently altered as a strange man enters her life."
,"The smooth life of a elderly woman will be changed completely as a neighbor enters her life."]
durations = [ x  for x in range(90,180)]
actors = ["Harrison Ford","Bob Ross","Hugh Jogh","Will Smith","Tom Hanks","Brad Smith","Angelina Jolie","Matt Damon"
,"Christian Bale","Clint Eastwood","Al Pacino","Tom Hardy","Ben Affleck"]
genres = ["action","mystery","thriller","comedy","fantasy","historical","animtaion"]

def generate_movies(db):
    x = 0 
    while x < len(titles) - 1:
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
    movie_count = len(db.get_movies())
    user_count = len(db.get_users())
    while x < 100:
        user_id = randrange(1,user_count+1)
        movie_id = randrange(1,movie_count+1)
        score = randrange(1,11)
        if db.add_review(user_id,movie_id,score) is True:
            x += 1

if __name__ == '__main__':
  db = Database('filmweb.db')
  db.clear()
  generate_users(db)
  generate_movies(db)
  generate_reviews(db)
  
        