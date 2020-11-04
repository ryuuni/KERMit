from server.server import app      # this dependency is necessary to prevent a circular import
from server.models.user import User
from server.config import UnitTestingConfig

app.config.from_object(UnitTestingConfig)


def test_hash_password():
    user = User('megfrenkel', 'testpass')
    assert user.hashed_password != 'testpass'
    assert user.username == 'megfrenkel'


def test_check_password_true():
    user = User('megfrenkel', 'testpass')
    assert user.check_password('testpass')


def test_check_password_false():
    user = User('megfrenkel', 'badpass')
    assert not user.check_password('testpass')
