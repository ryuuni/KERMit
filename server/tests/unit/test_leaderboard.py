"""
Unit tests for the Leaderboard Resource class.
"""
from flask import g
import pytest
from server.server import app
from server.config import UnitTestingConfig
from server.models.player import PuzzlePlayer
from server.models.user import User
from server.resources.leaderboard import Leaderboard

app.config.from_object(UnitTestingConfig)


@pytest.fixture
def user1():
    """
    Provide a test user to user within tests below
    """
    test_user = User(g_id='923423', first_name="Jane", last_name="Doe", email='janedoe1@tests.com')
    test_user.id = 1
    return test_user


def test_get_leaderboard_no_leaders(monkeypatch, user1):
    """
    Attempt to get a leaderboard, where there are no leaders yet because
    the no user in the whole system has finished a puzzle.
    """
    class MockParser:
        """Mock parsing class that accepts and parses a request."""
        def add_argument(self, *args, **kwargs):
            """Mock add argument"""
            return

        def parse_args(self):
            """Mock parse arguments, specifying specific test case"""
            return {'limit': None}

    def mock_get_top_players(*args, **kwargs):
        """Mock function that returns the resulting players that have finished sudoku puzzles"""
        return []

    monkeypatch.setattr(PuzzlePlayer, 'get_top_players', mock_get_top_players)

    with app.app_context():
        g.user = user1
        leaderboard_resource = Leaderboard()
        leaderboard_resource.parser = MockParser()
        result = leaderboard_resource.get()

    expected = {'message': 'No users have completed puzzles.', 'puzzles': []}
    assert result == expected


def test_get_leaderboard(monkeypatch, user1):
    """
    Test get leaderboard where there are several top players in the database.
    """
    class MockEntry:
        """
        A mock database entry that contains information about a user on the leaderboard.
        """
        def __init__(self, first_name, last_name, val):
            self.first_name = first_name
            self.last_name = last_name
            self.score = val

    class MockParser:
        """Mock parsing class that accepts and parses a request."""
        def add_argument(self, *args, **kwargs):
            """Mock add argument"""
            return

        def parse_args(self):
            """Mock parse arguments, specifying specific test case"""
            return {'limit': 2}

    def mock_get_top_players(*args, **kwargs):
        """Mock function that returns the resulting players that have finished sudoku puzzles"""
        return [MockEntry('foo', 'bar', 100), MockEntry('sally', 'sue', 50)]

    monkeypatch.setattr(PuzzlePlayer, 'get_top_players', mock_get_top_players)

    with app.app_context():
        g.user = user1
        leaderboard_resource = Leaderboard()
        leaderboard_resource.parser = MockParser()
        result = leaderboard_resource.get()

    expected = {'players': [{'first_name': 'foo', 'last_name': 'bar', 'score': 100},
                            {'first_name': 'sally', 'last_name': 'sue', 'score': 50}]}
    assert result == expected
