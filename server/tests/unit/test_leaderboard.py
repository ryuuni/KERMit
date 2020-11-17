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
    test_user = User(g_id='923423', first_name="Jane", last_name="Doe", email='janedoe1@tests.com')
    test_user.id = 1
    return test_user


def test_get_leaderboard_no_leaders(monkeypatch, user1):

    class MockParser:
        def add_argument(self, *args, **kwargs):
            pass

        def parse_args(self):
            return {'limit': None}

    def mock_get_top_players(*args, **kwargs):
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
    class MockEntry:
        def __init__(self, first_name, last_name, sum):
            self.first_name = first_name
            self.last_name = last_name
            self.score = sum

    class MockParser:
        def add_argument(self, *args, **kwargs):
            pass

        def parse_args(self):
            return {'limit': 2}

    def mock_get_top_players(*args, **kwargs):
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
