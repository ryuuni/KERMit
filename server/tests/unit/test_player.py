"""
Unit tests for the Player class.
"""
import pytest
from backend import app, db
from backend.config import UnitTestingConfig
from backend.models.puzzle_exception import PuzzleException
from backend.models.player import PuzzlePlayer
from backend.models.user import User
from tests.unit.mocks import MockSession

app.config.from_object(UnitTestingConfig)


class MockResults:
    """
    Class to mock query results; has same methods but just stubs that don't do anything.
    """
    def all(self):
        """
        Mock all method
        """
        return []

    def filter_by(self, *args, **kwargs):
        """
        Mock filter method
        """
        return MockResults()


class MockBaseQuery:
    """Class to mock query; has same methods but just stubs that don't do anything"""
    def __init__(self, *args, **kwargs):
        """
        Mock all method
        """

    def filter_by(self, *args, **kwargs):
        """
        Mock filter method
        """
        return MockResults()

    def join(self, *args, **kwargs):
        """
        Mock join method
        """
        return MockResults()


@pytest.fixture
def find_player_mock(monkeypatch):
    """
    Mock find player by g_id from the database with a predefined user.
    """
    def mock_find_player(*args):
        user = User('923423', first_name="Tester", last_name="Tester", email='test@tests.com')
        user.id = 1
        return user

    monkeypatch.setattr(User, "find_by_g_id", mock_find_player)


def test_save_commit(monkeypatch):
    """
    This test is mostly mocks; tests ensure the relevant classes/method are understood.
    """
    monkeypatch.setattr(db, "session", MockSession)
    player = PuzzlePlayer(1, 1)
    player.save(autocommit=True)
    assert True  # just want to make sure we can get here


def test_save(monkeypatch):
    """
    This test is mostly mocks; tests ensure the relevant classes/method are understood.
    """
    monkeypatch.setattr(db, "session", MockSession)
    player = PuzzlePlayer(1, 1)
    player.save(autocommit=False)
    assert True  # just want to make sure we can get here


def test_find_all_puzzles_for_player(monkeypatch, find_player_mock):
    """
    This test is mostly mocks; tests ensure the relevant classes/method are understood.
    """
    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)

    result = PuzzlePlayer.find_all_puzzles_for_player('923423')
    expected = []
    assert result == expected


def test_find_all_puzzles_for_player_hidden_only(monkeypatch, find_player_mock):
    """
    This test is mostly mocks; tests sure that hidden only is OK to use.
    """
    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)

    result = PuzzlePlayer.find_all_puzzles_for_player('923423', hidden_only=True)
    expected = []
    assert result == expected


def test_find_all_puzzles_for_player_visible_only(monkeypatch, find_player_mock):
    """
    This test is mostly mocks; tests sure that visible only is OK to use.
    """
    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)

    result = PuzzlePlayer.find_all_puzzles_for_player('923423', visible_only=True)
    expected = []
    assert result == expected


def test_find_all_puzzles_for_player_visible_and_hidden(monkeypatch, find_player_mock):
    """
    This test is mostly mocks; tests that using hidden and visible (an expected choice)
    still results in a reasonable output without error.
    """
    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)

    result = PuzzlePlayer.find_all_puzzles_for_player('923423', hidden_only=True, visible_only=True)
    expected = []
    assert result == expected


def test_find_players_for_puzzle(monkeypatch):
    """
    This test is mostly mocks; tests ensure the relevant classes/method are understood.
    """
    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    result = PuzzlePlayer.find_players_for_puzzle(1)
    assert result == []


def test_add_player_to_puzzle_already_too_many_players(monkeypatch):
    """
    Attempt to add a player to puzzle when there are already the maximum number of
    players (4) should fail.
    """
    def mock_return_existing_players(*args, **kwargs):
        user1 = User('923423', first_name="Tester1", last_name="Tester1", email='test1@tests.com')
        user2 = User('12345', first_name="Tester2", last_name="Tester2", email='tes2t@tests.com')
        user3 = User('912311', first_name="Tester3", last_name="Tester3", email='test3@tests.com')
        user4 = User('982363', first_name="Tester4", last_name="Tester4", email='test4@tests.com')
        return [user1, user2, user3, user4]

    monkeypatch.setattr(PuzzlePlayer, "find_players_for_puzzle", mock_return_existing_players)
    requesting_user = User('923423', first_name="Requester",
                           last_name="Requester", email='requester@tests.com')

    with pytest.raises(PuzzleException):
        PuzzlePlayer.add_player_to_puzzle(1, requesting_user)


def test_add_player_to_puzzle_player_doesnt_exist(monkeypatch):
    """
    An attempt to add a player to a puzzle that doesn't actually exist should fail.
    """
    def mock_return_existing_players(*args, **kwargs):
        return []

    monkeypatch.setattr(PuzzlePlayer, "find_players_for_puzzle", mock_return_existing_players)
    requesting_user = User('923423', first_name="Requester",
                           last_name="Requester", email='requester@tests.com')

    with pytest.raises(PuzzleException):
        PuzzlePlayer.add_player_to_puzzle(1, requesting_user)


def test_add_player_to_puzzle_ok(monkeypatch):
    """
    A valid attempt to add a player to a puzzle should be successful.
    """
    def mock_return_existing_players(*args, **kwargs):
        """
        Mock return existing players for the request.
        """
        user1 = User('923423', first_name="Tester1",
                     last_name="Tester1", email='test1@tests.com')
        user2 = User('12345', first_name="Tester2",
                     last_name="Tester2", email='tes2t@tests.com')
        return [user1, user2]

    monkeypatch.setattr(db, "session", MockSession)
    monkeypatch.setattr(PuzzlePlayer, "find_players_for_puzzle", mock_return_existing_players)
    requesting_user = User('923423', first_name="Requester",
                           last_name="Requester", email='requester@tests.com')

    PuzzlePlayer.add_player_to_puzzle(1, requesting_user)
    assert True  # just need to make sure we can get to this point


def test_to_player_to_str():
    """
    Test get player as string.
    """
    player = PuzzlePlayer(1, 1)
    assert str(player) == 'PuzzlePlayer(player_id=1, puzzle_id=1)'
