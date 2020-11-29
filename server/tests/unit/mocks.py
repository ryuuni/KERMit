"""
Mock Session class for testing.
"""
import pytest
from backend.google_auth import GoogleAuth
from backend.models.puzzle_pieces import PuzzlePiece
from backend.models.player import PuzzlePlayer
from backend.models.puzzle_exception import PuzzleException
from backend.models.sudoku_puzzle import Puzzle
from backend.models.user import User


class MockSession:
    """
    A class to provide easy mocking for sqlalchemy database sessions during testing.
    """
    def __init__(self, *args, **kwargs):
        self.value = None
        self.args = args
        self.kwargs = kwargs

    def add(self):
        """
        Mock add method
        """
        return

    @staticmethod
    def commit():
        """
        Mock commit method
        """
        return

    @staticmethod
    def flush():
        """
        Mock flush method
        """
        return

    @staticmethod
    def remove():
        """
        Mock remove method
        """
        return


@pytest.fixture
def user():
    """
    Create a test user
    """
    test_user = User(g_id='923423', first_name="Jane", last_name="Doe", email='janedoe1@tests.com')
    test_user.id = 1
    return test_user


@pytest.fixture
def mock_no_puzzles_for_player(monkeypatch):
    """
    Mock the find_all_puzzles_for_player() function, returning no puzzles for player.
    """
    def mock_get_puzzles_for_player(*args, **kwargs):
        return []

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)


@pytest.fixture
def mock_single_puzzles_for_player(monkeypatch):
    """
    Mock the find_all_puzzles_for_player() function, returning a single puzzle for player.
    """
    def mock_get_puzzles_for_player(*args, **kwargs):
        return [PuzzlePlayer(1, 1)]

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)


@pytest.fixture
def mock_get_puzzle(monkeypatch):
    """
    Mock get_puzzle() method by passing back a puzzle with known configuration.
    """
    def mock_get_puzzle(*args, **kwargs):
        puzzle = Puzzle(difficulty_level=0.5, completed=False, size=3)
        puzzle.puzzle_pieces = [PuzzlePiece(1, 0, 1, value=None, static_piece=False),
                                PuzzlePiece(1, 1, 1, value=3, static_piece=True)]
        return puzzle

    monkeypatch.setattr(Puzzle, 'get_puzzle', mock_get_puzzle)


@pytest.fixture
def mock_save(monkeypatch):
    """
    Mock save for puzzle and puzzle player
    """
    def save_mock(*args, **kwargs):
        """Helper mock"""
        return 1
    monkeypatch.setattr(Puzzle, 'save', save_mock)
    monkeypatch.setattr(PuzzlePlayer, 'save', save_mock)


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


@pytest.fixture
def mock_find_by_g_id(monkeypatch):
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
