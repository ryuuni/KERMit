from server.server import app    # prevent circular inports
from server.models.user import User
from server.resources.google_auth import GoogleAuth
import pytest
import os
from server.tests.integration.test_setup import test_client, init_db
from server.tests.integration.integration_mocks import verification_true, verification_error


@pytest.fixture(scope="function", autouse=False)
def user_info(monkeypatch):
    """Monkeypatch the google auth that obtains user info"""
    def mock_user_info(*args, **kwargs):
        return {
            "id": "103207744267402488580",
            "email": "janedoe@columbia.edu",
            "verified_email": True,
            "name": "Jane Doe",
            "given_name": "Jane",
            "family_name": "Doe",
            "picture": "https://lh3.googleusercontent.com/a-/AOh14Gh2my8WQqJudGC0Ft2A1Q-jrnVtxYTyrQkrIj6LNVU=s91-c",
            "locale": "en",
            "hd": "columbia.edu"
        }

    monkeypatch.setattr(GoogleAuth, "get_user_information", mock_user_info)


@pytest.fixture(scope="function", autouse=False)
def user_info_error(monkeypatch):
    """Monkeypatch the google auth that obtains user info"""
    def mock_user_info(*args, **kwargs):
        return {
            "error": {
                "code": 401,
                "message": "Request is missing required authentication credential. "
                           "Expected OAuth 2 access token, login cookie or other valid authentication credential. "
                           "See https://developers.google.com/identity/sign-in/web/devconsole-project.",
                "status": "UNAUTHENTICATED"
            }
        }

    monkeypatch.setattr(GoogleAuth, "get_user_information", mock_user_info)


def test_registration_missing_header(test_client, init_db):
    """
    Test when a request is made to /register that is missing the request header
    that contains the Google Access token.
    """
    response = test_client.post('/register')
    assert response.status_code == 400
    assert response.json == {'message': 'Request denied access',
                             'reason': 'Authorization header missing. Please provide an OAuth2 Token with your request'}


def test_registration_malformed_header(test_client, init_db):
    """
    Test when a request is made to /register that has mal-formatted request header
    that contains the Google Access token.
    """
    response = test_client.post('/register', headers={'Authorization': '2342351231asdb'})
    assert response.status_code == 400
    assert response.json == {'message': 'Request denied access',
                             'reason': "Malformed authorization header provided. Please make sure to specify "
                                       "the header prefix correctly as 'Bearer ' and try again."}


def test_registration_verification_token_invalid(test_client, init_db, verification_error):
    """
    Test when a request is made to /register that has a bad token.
    """
    response = test_client.post('/register', headers={'Authorization': 'Bearer 2342351231asdb'})
    assert response.status_code == 401
    assert response.json == {'message': 'Request denied access',
                             'reason': 'Google rejected oauth2 token: Invalid Value'}


def test_registration_user_info_error(test_client, init_db, verification_true, user_info_error):
    """
    Test when a request is made to /register, but the user info Google endpoint returned an error.
    """
    response = test_client.post('/register', headers={'Authorization': 'Bearer 2342351231asdb'})
    assert response.status_code == 401
    assert response.json == {'message': 'User could not be registered',
                             'reason': 'User identity could not be found; valid OAuth2 access token not received.'}


def test_registration_token_valid_missing_info1(monkeypatch, test_client, init_db, verification_true):
    """
    Test when verification of the token succeeds, but user information collection fails
    """
    def mock_user_info(*args, **kwargs):
        return {
            "id": "103207744267402488580",
            "verified_email": True,
            "name": "Jane Doe",
            "given_name": "Jane",
            "family_name": "Doe",
            "picture": "https://lh3.googleusercontent.com/a-/AOh14Gh2my8WQqJudGC0Ft2A1Q-jrnVtxYTyrQkrIj6LNVU=s91-c",
            "locale": "en",
            "hd": "columbia.edu"
        }
    monkeypatch.setattr(GoogleAuth, "get_user_information", mock_user_info)

    response = test_client.post('/register', headers={'Authorization': 'Bearer 2342351231asdb'})
    assert response.status_code == 401
    assert response.json == {'message': 'User could not be registered',
                             'reason': 'Google id (unique user identifier) and email must be retrievable attributes, '
                                       'but Google would not provide them.'}


def test_registration_token_valid_missing_info2(monkeypatch, test_client, init_db, verification_true):
    """
    Test when verification of the token succeeds, but user information collection fails
    """
    def mock_user_info(*args, **kwargs):
        return {
            "email": "janedoe@columbia.edu",
            "verified_email": True,
            "name": "Jane Doe",
            "given_name": "Jane",
            "family_name": "Doe",
            "picture": "https://lh3.googleusercontent.com/a-/AOh14Gh2my8WQqJudGC0Ft2A1Q-jrnVtxYTyrQkrIj6LNVU=s91-c",
            "locale": "en",
            "hd": "columbia.edu"
        }

    monkeypatch.setattr(GoogleAuth, "get_user_information", mock_user_info)

    response = test_client.post('/register', headers={'Authorization': 'Bearer 2342351231asdb'})
    assert response.status_code == 401
    assert response.json == {'message': 'User could not be registered',
                             'reason': 'Google id (unique user identifier) and email must be retrievable attributes, '
                                       'but Google would not provide them.'}


def test_registration_user_id_already_exists(monkeypatch, test_client, init_db, verification_true):
    """
    Make sure that if the user id already exists, there is no need to re-register them.
    """
    def mock_user_info(*args, **kwargs):
        return {
            "id": "12345",  # this user already exists
            "email": "janedoe@columbia.edu",
        }

    monkeypatch.setattr(GoogleAuth, "get_user_information", mock_user_info)

    response = test_client.post('/register', headers={'Authorization': 'Bearer 2342351231asdb'})
    assert response.status_code == 200
    assert response.json == {'message': 'User with Google ID 12345 is already registered.'}


def test_successful_user_registration(test_client, init_db, verification_true, user_info):
    """
    Make sure that a valid request to register a user is successful.
    """
    response = test_client.post('/register', headers={'Authorization': 'Bearer 2342351231asdb'})
    assert response.status_code == 200
    assert response.json == {'message': 'User Jane Doe was successfully registered'}
