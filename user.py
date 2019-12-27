

class User :
    def __init__(self,login,email,password):
        self.login = login
        self.email = email
        self.password = password

    def get_login(self):
        return self.login

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password