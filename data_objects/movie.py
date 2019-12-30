from data_objects.user import User

class Movie :
    def __init__(self,title,director,description,duration,actors,genre,icon_path = None,id = None):
        self.id = id
        self.title = title
        self.director = director
        self.description = description
        self.duration = duration
        self.actors = actors
        self.genre = genre
        self.icon_path = icon_path
        self.avg_rate = 0 
        self.number_of_users = 0

    def set_avg_rate(self,avg_rate , number_of_users):
        self.avg_rate = avg_rate
        self.number_of_users = number_of_users

    def rate(self,value,user):
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

    def get_actors(self):
        return self.actors

    def get_genre(self):
        return self.actors

    def get_id(self):
        return self.id

    def get_icon_path(self):
        return self.icon_path