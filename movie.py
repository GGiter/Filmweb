from user import User

class Movie :
    def __init__(self,id,title,director):
        self.id = id
        self.title = title
        self.director = director
        self.avg_rate = 0 
        self.number_of_users = 0

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

    def get_id(self):
        return self.id