from data_objects.movie import Movie
from data.database import Database
from random import randrange


class DataGenerator():
    def __init__(self, database):
        self.database = database
        if self.database:
            self.database.clear()

    def generate_users(self):

        if self.database is None:
            return

        emails_prefixs = ["gonzo", "bonzo", "kapelusz", "szalik", "zajac",
                          "internet", "abatoir", "abbadon", "slark", "renifer"]
        emails_suffixs = ["net.com", "gmail.com", "pw.pl", "internet"]
        logins = ["gonzo", "bonzo", "kapelusz", "szalik", "zajac", "internet",
                  "marszalek", "skyr", "ross", "Arrosive", "Bracteate",
                  "Juramentum", "Gallivant", "Contraband",
                  "Trochoid", "CshootBlithe"]
        passwords = ["rogalik", "renifer", "skyrim", "kapelusz", "wonsz"]

        x = 0
        while x < len(logins):
            email = ""
            email += emails_prefixs[randrange(len(emails_prefixs))]
            email += "@"
            email += emails_suffixs[randrange(len(emails_suffixs))]
            login = logins[randrange(len(logins))]
            password = passwords[randrange(len(passwords))]
            if self.database.register_user(login, email, password) is None:
                x += 1

    def generate_movies(self):

        if self.database is None:
            return

        titles = ["Honolulu", "Escape", "Great Escape", "Monkey", "Bones",
                  "Joker", "Zootopia", "The Jungle Book", "Bohemian",
                  "Skyfall", "Iron man", "Minions", "Toy Story",
                  "Incredibles", "Incredibles 2", "Jurrasic World",
                  "Jurrasic World 2", "Rayman", "Spectre", "Casino Royale",
                  "Lampion", "Reddit", "Bubble", "Frozen", "Frozen 2",
                  "Frozen 3", "Incredibles 3"]
        directors = ["Andrew Jack", "Bob Ross",
                     "Hugh Jogh", "Tim Burton", "Hugh Jackson",
                     "Woody Allen", "James Cameron"]
        descriptions = ["Sympathetic teacher DCI HANNAH COCKLE is arguing with"
                        "delightful teacher DR ZACH DONALDSON. HANNAH tries"
                        "to hug ZACH but he shakes her off.",
                        "The relaxed life of a woman take a sharp turn as"
                        "a friendly acquaintance enters her life.",
                        "The rough life of a woman will be changed"
                        "completely as a strange woman enters her life."]
        durations = [x for x in range(90, 180)]
        actors = ["Harrison Ford", "Bob Ross", "Hugh Jogh", "Will Smith",
                  "Tom Hanks", "Brad Smith", "Angelina Jolie", "Matt Damon",
                  "Christian Bale", "Clint Eastwood", "Al Pacino",
                  "Tom Hardy", "Ben Affleck"]
        genres = ["action", "mystery", "thriller",
                  "comedy", "fantasy", "historical", "animtaion"]

        x = 0
        while x < len(titles) - 1:
            title = titles[randrange(len(titles))]
            director = directors[randrange(len(directors))]
            description = descriptions[randrange(len(descriptions))]
            duration = durations[randrange(len(durations))]
            genre = genres[randrange(len(genres))]

            y = randrange(1, int(len(actors)/2))
            y += 1
            temporal_actors = actors.copy()
            actors_string = ""
            while y > 0:
                new_actor = temporal_actors[randrange(len(temporal_actors))]
                actors_string += f'{new_actor},'
                temporal_actors.remove(new_actor)
                y = y - 1

            actors_string = actors_string[:-1]

            if self.database.add_movie(Movie(title, director, description,
                                             duration, actors_string,
                                             genre)) is True:
                x += 1

    def generate_reviews(self):

        if self.database is None:
            return

        x = 0
        movie_count = len(self.database.get_movies())
        user_count = len(self.database.get_users())
        while x < 120:
            user_id = randrange(1, user_count+1)
            movie_id = randrange(1, movie_count+1)
            score = randrange(1, 11)
            if self.database.add_review(user_id, movie_id, score) is True:
                x += 1


if __name__ == '__main__':
    data_generator = DataGenerator(Database('filmweb.db'))
    data_generator.generate_users()
    data_generator.generate_movies()
    data_generator.generate_reviews()
