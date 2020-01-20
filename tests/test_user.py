from data_objects.user import User


def test_login():
    user1 = User(0, "", "")
    user2 = User("Mike", "", "")
    assert user1.get_login() == ""
    assert user2.get_login() == "Mike"


def test_password():
    user1 = User("", "", 0)
    user2 = User("", "", "password")
    assert user1.get_password() == ""
    assert user2.get_password() == "password"


def test_email():
    user1 = User("", "test", "")
    user2 = User("", 0, "")
    user3 = User("", "test@gmail.com", "")
    assert user1.get_email() == ""
    assert user2.get_email() == ""
    assert user3.get_email() == "test@gmail.com"
