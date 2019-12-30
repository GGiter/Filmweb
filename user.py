

class User :
    def __init__(self,login,email,password,id = None):
        self.login = login
        self.email = email
        self.password = password
        self.id = id

    def get_login(self):
        return self.login

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_id(self):
        return self.id 