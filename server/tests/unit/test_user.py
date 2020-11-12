import pytest
from server.server import app, db     # this dependency is necessary to prevent a circular import
from server.models.user import User
from server.tests.unit.mock_session import MockSession
from server.config import UnitTestingConfig

app.config.from_object(UnitTestingConfig)


@pytest.fixture
def user():
    user = User('103207743267402488580', 'Megan', 'Frenkel', 'mmf2171@columbia.edu')
    user.id = 1
    return user


def test_create_user(user):
    assert user.last_name == 'Frenkel'
    assert user.first_name == 'Megan'
    assert user.email == 'mmf2171@columbia.edu'
    assert user.g_id == '103207743267402488580'


def test_user_as_str(user):
    assert user.as_str() == 'Megan Frenkel (id = 1)'


def test_user_print(user):
    assert str(user) == 'User(first_name=Megan, last_name=Frenkel, id=1)'


def test_user_save(user, monkeypatch):
    monkeypatch.setattr(db, "session", MockSession)
    user.save()
    assert True   # just ensure we can get to here


def test_find_by_g_id(monkeypatch, user):
    class MockBaseQuery:
        def __init__(self, *args, **kwargs):
            pass

        def filter_by(self, *args, **kwargs):
            class Results():
                def first(self):
                    return user

            return Results()

        def join(self, *args, **kwargs):
            return

    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    result = User.find_by_g_id(1)
    expected = user
    assert expected == result

