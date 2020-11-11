from flask import g
import pytest
from server.config import UnitTestingConfig
from server.server import app, db
from server.models.user import User
from server.resources.authentication import Registration
from server.tests.unit.mock_session import MockSession

app.config.from_object(UnitTestingConfig)


@pytest.fixture
def get_user(monkeypatch):
    def mock_find_user(*args, **kwargs):
        return User(g_id="103207743267472488580", first_name='Jane', last_name='Doe', email='janedoe@columbia.edu')

    monkeypatch.setattr(User, 'find_by_g_id', mock_find_user)


def test_register(get_user):

    class MockGoogleAuth:
        def get_user_information(*args, **kwargs):
            return {
                "id": "103207743267472488580",
                "email": "janedoe@columbia.edu",
                "verified_email": True,
                "name": "Jane Doe",
                "given_name": "Jane",
                "family_name": "Doe",
                "picture": "https://lh3.googleusercontent.com/a-/AOh14Gh2my8WQqJud"
                           "GC0Ft2A1Q-jrnVtxYTyrQkrIj6LNVU=s91-c",
                "locale": "en",
                "hd": "columbia.edu"
            }

    with app.app_context():
        g.access_token = "access_token"
        registration = Registration()
        registration.google_auth = MockGoogleAuth()
        result = registration.post()

    expected = {'message': f'User with Google ID 103207743267472488580 is already registered.'}
    assert result == expected


def test_register_missing_info_email(get_user):

    class MockGoogleAuth:
        def get_user_information(*args, **kwargs):
            return {
                "id": "103207743267472488580",
                "verified_email": True,
                "name": "Jane Doe",
                "given_name": "Jane",
                "family_name": "Doe",
                "picture": "https://lh3.googleusercontent.com/a-/AOh14Gh2my8WQqJud"
                           "GC0Ft2A1Q-jrnVtxYTyrQkrIj6LNVU=s91-c",
                "locale": "en",
                "hd": "columbia.edu"
            }

    with app.app_context():
        g.access_token = "access_token"
        registration = Registration()
        registration.google_auth = MockGoogleAuth()
        result = registration.post()

    expected = ({'message': 'User could not be registered',
                 'reason': 'Google id (unique user identifier) and email must be retrievable attributes, '
                           'but Google would not provide them.'}, 401)
    assert result == expected


def test_register_missing_info_id(get_user):

    class MockGoogleAuth:
        def get_user_information(*args, **kwargs):
            return {
                "email": "janedoe@columbia.edu",
                "verified_email": True,
                "name": "Jane Doe",
                "given_name": "Jane",
                "family_name": "Doe",
                "picture": "https://lh3.googleusercontent.com/a-/AOh14Gh2my8WQq"
                           "JudGC0Ft2A1Q-jrnVtxYTyrQkrIj6LNVU=s91-c",
                "locale": "en",
                "hd": "columbia.edu"
            }

    with app.app_context():
        g.access_token = "access_token"
        registration = Registration()
        registration.google_auth = MockGoogleAuth()
        result = registration.post()

    expected = ({'message': 'User could not be registered',
                 'reason': 'Google id (unique user identifier) and email must be retrievable attributes, '
                           'but Google would not provide them.'}, 401)
    assert result == expected


def test_register_error_googleauth(get_user):

    class MockGoogleAuth:
        def get_user_information(*args, **kwargs):
            return {
                "error": {
                    "code": 401,
                    "message": "Request is missing required authentication credential. "
                               "Expected OAuth 2 access token, login cookie or other valid authentication "
                               "credential. See https://developers.google.com/identity/"
                               "sign-in/web/devconsole-project.",
                    "status": "UNAUTHENTICATED"
                }
            }

    with app.app_context():
        g.access_token = "access_token"
        registration = Registration()
        registration.google_auth = MockGoogleAuth()
        result = registration.post()

    expected = ({'message': 'User could not be registered',
                 'reason': 'User identity could not be found; valid OAuth2 access '
                           'token not received.'}, 401)
    assert result == expected


def test_register_exception(get_user):

    class MockGoogleAuth:
        def get_user_information(*args, **kwargs):
            raise Exception("Unknown Exception")

    with app.app_context():
        g.access_token = "access_token"
        registration = Registration()
        registration.google_auth = MockGoogleAuth()
        result = registration.post()

    expected = ({'message': 'User could not be registered',
                 'reason': 'Could not determine user information from Google '
                           'using Oath2 tokenfor unknown reason'}, 500)
    assert result == expected


def test_register_no_user_yet(monkeypatch):

    class MockGoogleAuth:
        def get_user_information(*args, **kwargs):
            return {
                "id": "103207743267472488580",
                "email": "janedoe@columbia.edu",
                "verified_email": True,
                "name": "Jane Doe",
                "given_name": "Jane",
                "family_name": "Doe",
                "picture": "https://lh3.googleusercontent.com/a-/AOh14Gh2my8WQq"
                           "JudGC0Ft2A1Q-jrnVtxYTyrQkrIj6LNVU=s91-c",
                "locale": "en",
                "hd": "columbia.edu"
            }

    monkeypatch.setattr(User, 'find_by_g_id', lambda x: None)
    monkeypatch.setattr(User, 'save', lambda x: None)
    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        g.access_token = "access_token"
        registration = Registration()
        registration.google_auth = MockGoogleAuth()
        result = registration.post()

    expected = {'message': 'User Jane Doe was successfully registered'}
    assert result == expected


def test_register_exception_db(monkeypatch):

    class MockGoogleAuth:
        def get_user_information(*args, **kwargs):
            return {
                "id": "103207743267472488580",
                "email": "janedoe@columbia.edu",
                "verified_email": True,
                "name": "Jane Doe",
                "given_name": "Jane",
                "family_name": "Doe",
                "picture": "https://lh3.googleusercontent.com/a-/AOh14Gh2my8WQqJ"
                           "udGC0Ft2A1Q-jrnVtxYTyrQkrIj6LNVU=s91-c",
                "locale": "en",
                "hd": "columbia.edu"
            }

    def raise_exception():
        raise Exception("some execption")

    monkeypatch.setattr(User, 'find_by_g_id', lambda x: None)
    monkeypatch.setattr(User, 'save', raise_exception)
    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        g.access_token = "access_token"
        registration = Registration()
        registration.google_auth = MockGoogleAuth()
        result = registration.post()

    expected = ({'message': 'User could not be registered.',
                 'reason': 'An unknown error occurred raise_exception() takes 0 '
                           'positional arguments but 1 was given'},
                500)
    assert result == expected
