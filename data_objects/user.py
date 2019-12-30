

class User :
    def __init__(self,login,email,password,icon_path = None , id = None):
        self.login = login
        self.email = email
        self.password = password
        self.icon_path = icon_path
        self.id = id

    def get_login(self):
        return self.login

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_id(self):
        return self.id 

    def get_icon_path(self):
        return self.icon_path