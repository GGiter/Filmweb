from data.database import Database
from data_objects.user import User

def test_login():
    user = User(0,"","")
    assert user.get_login() == ""


def test_password():
    user = User("",0,"")
    assert user.get_password() == ""


def test_email():
    user1 = User("","","test")
    user2 = User("","",0)
    assert user1.get_email() == ""
    assert user2.get_email() == ""