"""
Shared integration tests mocks used in multiple test cases
"""
import pytest
from server.resources.google_auth import GoogleAuth


@pytest.fixture(scope="function", autouse=False)
def verification_true(monkeypatch):
    """
    Monkeypatch the google auth that verifies the token.
    """
    def mock_verification(*args, **kwargs):
        return {
            "issued_to": "984247564103-2vfoopeqjoqtd21tsp3namg9sijus9ai.apps.googleusercontent.com",
            "audience": "984247564103-2vfoopeqjoqtd21tsp3namg9sijus9ai.apps.googleusercontent.com",
            "user_id": "987234",
            "scope": "https://www.googleapis.com/auth/userinfo.email",
            "expires_in": 3588,
            "email": "jb@biden2020.com",
            "verified_email": True,
            "access_type": "offline"
        }

    monkeypatch.setattr(GoogleAuth, "validate_token", mock_verification)


@pytest.fixture(scope="function", autouse=False)
def verification_error(monkeypatch):
    """
    Monkeypatch the google auth that verifies the token.
    """
    def mock_verification(*args, **kwargs):
        return {
            "error": "invalid_token",
            "error_description": "Invalid Value"
        }

    monkeypatch.setattr(GoogleAuth, "validate_token", mock_verification)
