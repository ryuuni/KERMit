from server.server import app, db     # this dependency is necessary to prevent a circular import
from server.models.user import User


def test_hash_password():
    user = User('megfrenkel', 'testpass')
    assert user.hashed_password != 'testpass'
    assert user.username == 'megfrenkel'


def test_check_password_true():
    user = User('megfrenkel', 'testpass')
    assert User.check_password('testpass', user.hashed_password)


def test_check_password_false():
    user = User('megfrenkel', 'badpass')
    assert not User.check_password('testpass', user.hashed_password)
