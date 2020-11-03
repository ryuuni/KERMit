from server.server import app, db
from server.models.user import User
from server.config import TestingConfig
import pytest
import os
from server.tests.integration.test_setup import test_client, init_db


def test_registration_missing_user(test_client, init_db):
    """
    Test that when a request is made to /register that is missing the username, the request
    fails with the appropriate reason.
    """
    response = test_client.post('/register', data=dict(password='testertester'))
    assert response.status_code == 400
    assert response.json['message'] == {'username': 'The username field must be provided'}


def test_registration_missing_password(test_client, init_db):
    """
    Test that when a request is made to /register that is missing the password, the request
    fails with the appropriate reason.
    """
    response = test_client.post('/register', data=dict(username='tester'))
    assert response.status_code == 400
    assert response.json['message'] == {'password': 'The password field must be provided'}


def test_registration_valid(test_client, init_db):
    """
    Test that when a request is made to /register that has the appropriate information, the
    user is successfully created.
    """
    # check response
    response = test_client.post('/register', data=dict(username='tester', password='testertester'))
    assert response.status_code == 200
    assert response.json['message'] == 'User tester was successfully created'
    assert all(key in response.json.keys() for key in ['message', 'access_token', 'refresh_token'])

    # check data in db
    user = User.query.filter_by(username='tester').first()
    assert user.id == 1
    assert user.hashed_password is not None
    assert user.username == 'tester'


def test_registration_duplicate_user(test_client, init_db):
    """
    Test that when a request is made to /register that has the appropriate information, but
    a username that is already taken, the request fails.
    """
    response = test_client.post('/register', data=dict(username='tester', password='testertester'))
    assert response.status_code == 403
    assert "Username tester is already taken" in str(response.data)


def test_login_correct(test_client, init_db):
    """
    Test that when a request is made to /login that has the appropriate information,
    the user can successfully login and receive a set of tokens.
    """

    response = test_client.post('/login', data=dict(username='tester', password='testertester'))
    assert response.status_code == 200
    assert response.json['message'] == 'Logged in as tester'
    assert all(key in response.json.keys() for key in ['message', 'access_token', 'refresh_token'])


def test_login_user_doesnt_exist(test_client, init_db):
    """
    Test that when a request is made to /login that has a username that doesn't exist,
    a message is returned explaining the issue and user does not receive a token.
    """
    response = test_client.post('/login', data=dict(username='nonexistant_user', password='testertester'))
    assert response.status_code == 404
    assert response.json['message'] == 'User nonexistant_user does not exist'
    assert not any(key in response.json.keys() for key in ['access_token', 'refresh_token'])


def test_login_incorrect_pw(test_client, init_db):
    """
    Test that when a request is made to /login that has a bad password,
    a message is returned explaining the issue and user does not receive a token.
    """
    response = test_client.post('/login', data=dict(username='tester', password='badpass'))
    assert response.status_code == 401
    assert response.json['message'] == 'Incorrect password'
    assert not any(key in response.json.keys() for key in ['access_token', 'refresh_token'])


def test_refresh_token_valid(test_client, init_db):
    """
    Test that a user can refresh their token with a valid refresh token.
    """
    response = test_client.post('/login', data=dict(username='tester', password='testertester'))
    response = test_client.post('/refresh',
                                headers={'Authorization': 'Bearer {}'.format(response.json['refresh_token'])})
    assert response.status_code == 200
    assert 'access_token' in response.json.keys()


def test_refresh_token_invalid(test_client, init_db):
    """
    Test that a user cannot refresh their token without a valid refresh token (i.e., access tokens do not work)
    """
    response = test_client.post('/login', data=dict(username='tester', password='testertester'))
    response = test_client.post('/refresh',
                                headers={'Authorization': 'Bearer {}'.format(response.json['access_token'])})
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid token provided'


def test_log_out_access_valid(test_client, init_db):
    """
    Test that when a request is made to /logout, specifically to blacklist the access token, it is successfully
    added to the blacklist
    """
    first_resp = test_client.post('/login', data=dict(username='tester', password='testertester'))
    response = test_client.post('/logout/access',
                                headers={'Authorization': 'Bearer {}'.format(first_resp.json['access_token'])})
    assert response.status_code == 200

    second_resp = test_client.post('/logout/access',
                                   headers={'Authorization': 'Bearer {}'.format(first_resp.json['access_token'])})
    assert second_resp.status_code == 401
    assert second_resp.json['message'] == 'Token has been revoked'


def test_log_out_access_invalid(test_client, init_db):
    """
    Test that when a request is made to /logout, specifically to blacklist the access token, the token
    will be not added unless it is a valid access token
    """
    first_resp = test_client.post('/login', data=dict(username='tester', password='testertester'))
    response = test_client.post('/logout/access',
                                headers={'Authorization': 'Bearer {}'.format(first_resp.json['refresh_token'])})
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid token provided'


def test_log_out_refresh_valid(test_client, init_db):
    """
    Test that when a request is made to /logout, specifically to blacklist the access token, it is successfully
    added to the blacklist
    """
    first_resp = test_client.post('/login', data=dict(username='tester', password='testertester'))
    response = test_client.post('/logout/refresh',
                                headers={'Authorization': 'Bearer {}'.format(first_resp.json['refresh_token'])})
    assert response.status_code == 200
    second_resp = test_client.post('/logout/refresh',
                                   headers={'Authorization': 'Bearer {}'.format(first_resp.json['refresh_token'])})
    assert second_resp.status_code == 401
    assert second_resp.json['message'] == 'Token has been revoked'


def test_log_out_refresh_invalid(test_client, init_db):
    """
    Test that when a request is made to /logout, specifically to blacklist the access token, the token
    will be not added unless it is a valid access token
    """
    fake_token = '12345'
    response = test_client.post('/logout/refresh', headers={'Authorization': 'Bearer {}'.format(fake_token)})
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid token provided'

