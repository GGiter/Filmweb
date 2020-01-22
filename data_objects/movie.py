class Movie:
    """
    class that represents data about movie from database
    """
    def __init__(self, title, director, description, duration, actors,
                 genre, icon_path=None, id=None):
        self._id = id
        self._title = title if isinstance(title, str) else ""
        self._director = director if isinstance(director, str) else ""
        self._description = description if isinstance(description, str) else ""
        self._duration = abs(int(duration)) if self.is_duration_int(duration) else 0
        self._actors = actors if isinstance(actors, str) else ""
        self._genre = genre if isinstance(genre, str) else ""
        self._icon_path = icon_path if isinstance(genre, str) else ""
        self._avg_rate = 0
        self._number_of_users = 0

    def is_duration_int(self, duration):
        try:
            int(duration)
            return True
        except ValueError:
            return False

    def set_avg_rate(self, avg_rate, number_of_users):
        self._avg_rate = avg_rate
        self._number_of_users = number_of_users

    def rate(self, value, user):
        """
        Rate movie
        return False if fails
        return True if succeeds
        """
        if user is None:
            return False

        self._avg_rate *= self._number_of_users
        self._avg_rate += value
        self._number_of_users += 1
        self._avg_rate /= self._number_of_users
        self._avg_rate = int(self._avg_rate)

        return True

    def get_title(self):
        return self._title

    def get_director(self):
        return self._director

    def get_avg_rate(self):
        return self._avg_rate

    def get_description(self):
        return self._description

    def get_duration(self):
        return self._duration

    def get_actors(self):
        return self._actors

    def get_genre(self):
        return self._genre

    def get_id(self):
        return self._id

    def get_icon_path(self):
        return self._icon_path

    def is_valid(self):
        return (self._title != "" and self._director != ""
                and self._duration != 0)
