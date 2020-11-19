"""
Unit tests for the Google Auth class.
"""
import pytest
import requests
from server.resources.google_auth import GoogleAuth


class MockResponse:
    """
    Mock the response from API
    """
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """
        Mock return json data
        """
        return self.json_data


def test_validate_token(monkeypatch):
    """
    Validation of token should return json containing token information.
    """
    json = {
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

    def mock_response(*args, **kwargs):
        return MockResponse(json_data=json, status_code=200)

    monkeypatch.setattr(requests, "get", mock_response)
    google_auth = GoogleAuth()
    result = google_auth.validate_token("A fake token")
    assert json == result


def test_get_user_information(monkeypatch):
    """
    Retrieval of user information should return json containing token information.
    """
    json = {
        "email": "janedoe@columbia.edu",
        "verified_email": True,
        "name": "Jane Doe",
        "given_name": "Jane",
        "family_name": "Doe",
        "picture": "https://lh3.googleusercontent.com/a-/AOh14Gh2my8WQ"
                   "qJudGC0Ft2A1Q-jrnVtxYTyrQkrIj6LNVU=s91-c",
        "locale": "en",
        "hd": "columbia.edu"
    }

    def mock_response(*args, **kwargs):
        return MockResponse(json_data=json, status_code=200)

    monkeypatch.setattr(requests, "get", mock_response)
    google_auth = GoogleAuth()
    result = google_auth.get_user_information("A fake token")
    assert json == result
