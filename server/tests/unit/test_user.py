"""
Unit tests for User model.
"""
import pytest
from backend import app, db
from backend.config import UnitTestingConfig
from backend.models.user import User
from tests.unit.mocks import MockSession

app.config.from_object(UnitTestingConfig)


@pytest.fixture
def user():
    """
    Create test user.
    """
    user = User('103207743267402488580', 'Megan', 'Frenkel', 'mmf2171@columbia.edu')
    user.id = 1
    return user


def test_create_user(user):
    """
    Test the creation of a User instance.
    """
    assert user.last_name == 'Frenkel'
    assert user.first_name == 'Megan'
    assert user.email == 'mmf2171@columbia.edu'
    assert user.g_id == '103207743267402488580'


def test_user_as_str(user):
    """
    Test get user as a formatted string.
    """
    assert user.as_str() == 'Megan Frenkel (id = 1)'


def test_user_print(user):
    """
    Test print user.
    """
    assert str(user) == 'User(first_name=Megan, last_name=Frenkel, id=1)'


def test_user_save(user, monkeypatch):
    """
    Test save user, using mock for database session.
    """
    monkeypatch.setattr(db, "session", MockSession)
    user.save()
    assert True   # just ensure we can get to here


def test_find_by_g_id(monkeypatch, user):
    """
    Test find the User by g_id, mocking the database with a mock base query.
    """
    class MockBaseQuery:
        """
        Mock instance of Sqlachelmy base query
        """
        def __init__(self, *args, **kwargs):
            pass

        def filter_by(self, *args, **kwargs):
            """Mock filter by method"""
            class Results():
                """ Mock results class for mimicking base query results"""
                def first(self):
                    """Mock get first result"""
                    return user
            return Results()

        def join(self, *args, **kwargs):
            """ Mock join method, does nothing"""
            return

    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    result = User.find_by_g_id(1)
    expected = user
    assert expected == result


def test_find_users_by_email_none():
    """
    Test method when no additional emails are provided
    """
    assert User.find_users_by_email([]) == ([], [])


def test_find_users_by_email_one_found(monkeypatch, user):
    """
    Test method when additional email provided, and one found in database.
    """
    monkeypatch.setattr(User, "find_by_email", lambda x: user)
    assert User.find_users_by_email(['atestemail@emails.com']) == ([user], [])


def test_find_users_by_email_none_found(monkeypatch):
    """
    Test method when additional email provided, but not found in database.
    """
    monkeypatch.setattr(User, "find_by_email", lambda x: None)
    assert User.find_users_by_email(['atestemail@emails.com']) == ([], ['atestemail@emails.com'])


def test_get_email(monkeypatch, user):
    """
    Mock the base query class and call the get_email() function.
    """
    class MockBaseQuery:
        """
        Mock instance of Sqlachelmy base query
        """
        def __init__(self, *args, **kwargs):
            pass

        def filter_by(self, *args, **kwargs):
            """Mock filter by method"""
            class Results():
                """ Mock results class for mimicking base query results"""
                def first(self):
                    """Mock get first result"""
                    return user
            return Results()

        def join(self, *args, **kwargs):
            """ Mock join method, does nothing"""
            return

    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    assert User.find_by_email('atestemail@emails.com') == user
