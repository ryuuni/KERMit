import pytest
from server.config import UnitTestingConfig
from server.models.puzzle_exception import PuzzleException
from server.server import app, db
from server.models.player import PuzzlePlayer
from server.models.user import User
from server.tests.unit.mock_session import MockSession

app.config.from_object(UnitTestingConfig)


class MockResults:
    """Class to mock query results; has same methods but just stubs that don't do anything"""
    def all(self):
        return []

    def filter_by(self, *args, **kwargs):
        return MockResults()


class MockBaseQuery:
    """Class to mock query; has same methods but just stubs that don't do anything"""
    def __init__(self, *args, **kwargs):
        pass

    def filter_by(self, *args, **kwargs):
        return MockResults()

    def join(self, *args, **kwargs):
        return MockResults()


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


def test_find_all_puzzles_for_player(monkeypatch):
    """
    This test is mostly mocks; tests ensure the relevant classes/method are understood.
    """
    def mock_find_player(*args):
        user = User('923423', first_name="Tester", last_name="Tester", email='test@tests.com')
        user.id = 1
        return user

    def mock_query(*args):
        return []

    monkeypatch.setattr(User, "find_by_g_id", mock_find_player)
    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)

    result = PuzzlePlayer.find_all_puzzles_for_player('923423')
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
    Attempt to add a player to puzzle when there are already the maximum number of players (4) should fail.
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

    with pytest.raises(PuzzleException) as pe:
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

    with pytest.raises(PuzzleException) as pe:
        PuzzlePlayer.add_player_to_puzzle(1, requesting_user)


def test_add_player_to_puzzle_ok(monkeypatch):
    """
    A valid attempt to add a player to a puzzle should be successful.
    """

    def mock_return_existing_players(*args, **kwargs):
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
    player = PuzzlePlayer(1, 1)
    assert str(player) == 'PuzzlePlayer(player_id=1, puzzle_id=1)'
