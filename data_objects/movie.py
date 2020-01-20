class Movie:
    """
    class that represents data about movie from database
    """
    def __init__(self, title, director, description, duration, actors,
                 genre, icon_path=None, id=None):
        self.id = id
        self.title = title if isinstance(title, str) else ""
        self.director = director if isinstance(director, str) else ""
        self.description = description if isinstance(description, str) else ""
        self.duration = duration if isinstance(duration, int) else 0
        self.actors = actors if isinstance(actors, str) else ""
        self.genre = genre if isinstance(genre, str) else ""
        self.icon_path = icon_path if isinstance(genre, str) else ""
        self.avg_rate = 0
        self.number_of_users = 0

    def set_avg_rate(self, avg_rate, number_of_users):
        self.avg_rate = avg_rate
        self.number_of_users = number_of_users

    def rate(self, value, user):
        """
        Rate movie
        return False if fails
        return True if succeeds
        """
        if user is None:
            return False

        self.avg_rate *= self.number_of_users
        self.avg_rate += value
        self.number_of_users += 1
        self.avg_rate /= self.number_of_users
        self.avg_rate = int(self.avg_rate)

        return True

    def get_title(self):
        return self.title

    def get_director(self):
        return self.director

    def get_avg_rate(self):
        return self.avg_rate

    def get_description(self):
        return self.description

    def get_duration(self):
        return self.duration

    def get_actors(self):
        return self.actors

    def get_genre(self):
        return self.genre

    def get_id(self):
        return self.id

    def get_icon_path(self):
        return self.icon_path
