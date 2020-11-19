"""
Test Google Authentication mechanism
"""
from flask import g
import pytest
from server.config import UnitTestingConfig
from server.resources.google_auth import GoogleAuth
from server.server import app, db
from server.models.user import User
from server.resources.authentication import Registration, _verify_token
from server.tests.unit.mock_session import MockSession

app.config.from_object(UnitTestingConfig)


@pytest.fixture
def get_user(monkeypatch):
    """
    Mock the User.find_by_g_id() function.
    """
    def mock_find_user(*args, **kwargs):
        """
        Mock the find user method, providing back a user that can be
        used in further testing.
        """
        return User(g_id="103207743267472488580", first_name='Jane',
                    last_name='Doe', email='janedoe@columbia.edu')

    monkeypatch.setattr(User, 'find_by_g_id', mock_find_user)


@pytest.fixture
def verification_token(monkeypatch):
    """
    Mock verification of token that is valid.
    """
    def mock_verify_token(*args, **kwargs):
        """
        Return the content expected when a token is successfully verified.
        """
        return {
            "issued_to": "407408718192.apps.googleusercontent.com",
            "audience": "407408718192.apps.googleusercontent.com",
            "user_id": "103207743267402488580",
            "scope": "https://www.googleapis.com/auth/userinfo.email "
                     "https://www.googleapis.com/auth/userinfo.profile openid",
            "expires_in": 3590,
            "email": "mmf2171@columbia.edu",
            "verified_email": True,
            "access_type": "offline"
        }
    monkeypatch.setattr(GoogleAuth, "validate_token", mock_verify_token)


class MockGoogleAuth:
    """
    Mock google auth class that can be used to mock the case when
    the Google Auth API is able to successfully validate a Oauth token for a user
    and the user has provided access to their information.
    """

    def get_user_information(self, *args):
        """
        Mock get user information when token is valid and information is available.
        """
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


def test_authorize_token_missing_header():
    """
    Verification of token should fail if header is missing Authentication info.
    """
    class MockRequest:
        """Mock Request for verification of token."""
        def __init__(self):
            self.headers = {}

    result = _verify_token(MockRequest())
    expected = {'message': 'Request denied access',
                'reason': 'Authorization header missing. Please provide an '
                           'OAuth2 Token with your request'}, 400
    assert expected == result


def test_authorize_token_missing_header2():
    """
    Verification of token should fail if header is missing Authentication info.
    """
    class MockRequest:
        """Mock Request for verification of token."""
        def __init__(self):
            self.headers = {'Something': 'here'}

    result = _verify_token(MockRequest())
    expected = {'message': 'Request denied access',
                'reason': 'Authorization header missing. Please provide an '
                           'OAuth2 Token with your request'}, 400
    assert expected == result


def test_authorize_token_malformed_header():
    """
    Verification of token should fail if header is Authentication info is malformed
    """
    class MockRequest:
        """Mock Request for verification of token."""
        def __init__(self):
            self.headers = {'Authorization': 'Token here'}

    result = _verify_token(MockRequest())
    expected = {'message': 'Request denied access',
                'reason': "Malformed authorization header provided. Please make sure to "
                           "specify the header prefix correctly as 'Bearer ' and try again."}, 400
    assert expected == result


def test_authorize_token_validation_error(monkeypatch):
    """
    Verification of token should fail if header is Authentication info is malformed
    """
    class MockRequest:
        """Mock Request for verification of token."""
        def __init__(self):
            self.headers = {'Authorization': 'Bearer Token-Here'}

    def mock_verify_token(*args, **kwargs):
        """Mock the verification of the token fails."""
        return {"error": "some error", "error_description": 'A bad error occurred'}

    monkeypatch.setattr(GoogleAuth, "validate_token", mock_verify_token)

    result = _verify_token(MockRequest())
    expected = {'message': 'Request denied access',
                'reason': 'Google rejected oauth2 token: A bad error occurred'}, 401
    assert expected == result


def test_authorize_token_validation_success_register(verification_token):
    """
    Verification of token should fail if header is Authentication info is malformed
    """
    class MockRequest:
        """Mock Request for verification of token."""
        def __init__(self):
            self.headers = {'Authorization': 'Bearer Token-Here'}
            self.endpoint = 'registration'

    with app.app_context():
        result = _verify_token(MockRequest())
        assert result is None
        assert g.access_token == "Token-Here"


def test_authorize_token_validation_success(monkeypatch, verification_token):
    """
    Verification of token should fail if header is Authentication info is malformed
    """
    class MockRequest:
        """
        Mock Request for verification of token.
        """
        def __init__(self):
            self.headers = {'Authorization': 'Bearer Token-Here'}
            self.endpoint = 'sudoku'

    mock_user = User('103207743267402488580', 'Megan', 'Frenkel', 'mmf2171@columbia.edu')

    def mock_find_user(*args, **kwargs):
        """Mock find user when there is a user to find."""
        return mock_user

    monkeypatch.setattr(User, "find_by_g_id", mock_find_user)

    with app.app_context():
        result = _verify_token(MockRequest())
        assert result is None
        assert g.access_token == "Token-Here"
        assert g.user == mock_user


def test_authorize_token_validation_not_registered(monkeypatch, verification_token):
    """
    Verification of token should fail if header is Authentication info is malformed
    """
    class MockRequest:
        """
        Mock Request for verification of token.
        """
        def __init__(self):
            self.headers = {'Authorization': 'Bearer Token-Here'}
            self.endpoint = 'sudoku'

    def mock_find_user(*args, **kwargs):
        """
        Mock the scenario where the method that attempts to find users cannot find
        any matching users; the request should be denied.
        """
        return None

    monkeypatch.setattr(User, "find_by_g_id", mock_find_user)

    with app.app_context():
        result = _verify_token(MockRequest())

    expected = {'message': 'Request denied access',
                'reason': 'User is not yet registered with this application; please '
                          'register before proceeding'}, 401
    assert expected == result


def test_register(get_user):
    """
    Test register a user where the authentication of the token is successful.
    """
    with app.app_context():
        g.access_token = "access_token"
        registration = Registration()
        registration.google_auth = MockGoogleAuth()
        result = registration.post()

    expected = {'message': 'User with Google ID 103207743267472488580 is already registered.'}
    assert result == expected


def test_register_missing_info_email(get_user):
    """
    If user information retrieved from Google is missing the user's email, request should fail.
    """
    class MockGoogleAuth2:
        """
        Mock the google authentication class and results
        """
        def get_user_information(self, *args, **kwargs):
            """
            Expected user information, when there is a succesfull token validation
            but a required field is missing.
            """
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
        registration.google_auth = MockGoogleAuth2()
        result = registration.post()

    expected = ({'message': 'User could not be registered',
                 'reason': 'Google id (unique user identifier) and email must be retrievable '
                           'attributes, but Google would not provide them.'}, 401)
    assert result == expected


def test_register_missing_info_id(get_user):
    """
    If user information retrieved from Google is missing the user's id, request should fail.
    """
    class MockGoogleAuth:
        """
        Mock the google authentication class and results
        """
        def get_user_information(self, *args, **kwargs):
            """
            Expected user information, when there is a succesfull token validation
            but a required field is missing.
            """
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
                 'reason': 'Google id (unique user identifier) and email must be retrievable'
                            ' attributes, but Google would not provide them.'}, 401)
    assert result == expected


def test_register_error_googleauth(get_user):
    """
    If user information could not be retrieved from Google for any reason, request should fail.
    """
    class MockGoogleAuth:
        """
        Mock the google authentication class and results
        """
        def get_user_information(self, *args, **kwargs):
            """
            Expected user information, when there is an error that occurs in the validation
            of the Oauth token by the Google API
            """
            return {
                "error": {
                    "code": 401,
                    "message": "Request is missing required authentication credential. "
                               "Expected OAuth 2 access token, login cookie or other valid "
                               "authentication credential. "
                               "See https://developers.google.com/identity/"
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
    """
    If any exception is raised, the user should not be able to register.
    """
    class MockGoogleAuth:
        """
        Mock Google authentication to easily raise Exception
        """
        def get_user_information(self, *args, **kwargs):
            """Use this function to cause a function to raise an exception when called."""
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
    """
    If data is successfully retrieved from google for the user, they should be able to successfully
    register with the puzzle game.
    """
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
    """
    If an exception is raised during the processing of the registration, the user should be alerted.
    """
    def raise_exception():
        """Use this function to cause a function to raise an exception when called."""
        raise Exception("some exception")

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
