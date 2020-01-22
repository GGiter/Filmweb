class User:
    """
    class that represents data about user from database
    """
    def __init__(self, login, email, password, icon_path=None, id=None):
        self._login = login if isinstance(login, str) else ""
        self._email = email if self.is_email_valid(email) else ""
        self._password = password if isinstance(password, str) else ""
        self._icon_path = icon_path
        self._id = id

    def is_email_valid(self, email):
        if isinstance(email, str) and email.find("@") > -1:
            return True
        return False

    def get_login(self):
        return self._login

    def get_email(self):
        return self._email

    def get_password(self):
        return self._password

    def get_id(self):
        return self._id

    def get_icon_path(self):
        return self._icon_path
