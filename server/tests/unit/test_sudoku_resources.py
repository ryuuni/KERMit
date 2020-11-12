import pytest
from server.server import app, db
from server.models.player import PuzzlePlayer
from server.models.puzzle_exception import PuzzleException
from flask import g
from server.models.sudoku_puzzle import Puzzle
from server.models.user import User
from server.resources.sudoku import sudoku_to_dict, SudokuPuzzles, SudokuPuzzle
from server.config import UnitTestingConfig
from server.tests.unit.mock_session import MockSession

app.config.from_object(UnitTestingConfig)


@pytest.fixture
def user():
    test_user = User(g_id='923423', first_name="Jane", last_name="Doe", email='janedoe1@tests.com')
    test_user.id = 1
    return test_user


@pytest.fixture
def mock_no_puzzles_for_player(monkeypatch):
    def mock_get_puzzles_for_player(*args, **kwargs):
        return []

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)


@pytest.fixture
def mock_get_puzzle(monkeypatch):
    def mock_get_puzzle(*args, **kwargs):
        puzzle = Puzzle(difficulty_level=0.5, completed=False, size=3)
        puzzle.puzzle_pieces = []
        return puzzle

    monkeypatch.setattr(Puzzle, 'get_puzzle', mock_get_puzzle)


def test_sudoku_to_json():
    foobar = User('54321', 'foo', 'bar', 'foobar@comsci.com')
    foobar.id = 1

    princess = User('98734', 'Princess', 'Bride', 'princess@princessbride.com')
    princess.id = 2

    sudoku = Puzzle(difficulty_level=0.6, size=4)
    players = [foobar, princess]

    result = sudoku_to_dict(sudoku, players)

    # note that because you cannot predict what sudoku boards are created, not comparing pieces,
    # just for simplicity for now
    assert not result['puzzle_id']
    assert not result['completed']
    assert result['difficulty'] == 0.6
    assert result['point_value'] == 110
    assert result['players'] == [
        {'id': 1, 'first_name': 'foo', 'last_name': 'bar', 'email': 'foobar@comsci.com'},
        {'id': 2, 'first_name': 'Princess', 'last_name': 'Bride', 'email': 'princess@princessbride.com'}
    ]


def test_get_sudoku_puzzles_none(monkeypatch, mock_no_puzzles_for_player, user):

    with app.app_context():
        puzzles_resource = SudokuPuzzles()
        g.user = user
        result = puzzles_resource.get()

    expected = {
        'message': f'No sudoku puzzles are associated with Jane Doe (id = 1)',
        'puzzles': []
    }
    assert result == expected


def test_get_sudoku_puzzles_all(monkeypatch, user, mock_get_puzzle):

    def mock_get_puzzles_for_player(*args, **kwargs):
        return [PuzzlePlayer(player_id=5, puzzle_id=3)]

    def mock_get_players(*args, **kwargs):
        return [User(first_name='Sally', last_name='Sue', email='sallysue@emails.com', g_id='123445')]

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)
    monkeypatch.setattr(PuzzlePlayer, 'find_players_for_puzzle', mock_get_players)

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        result = puzzles_resource.get()

    expected = {
        'puzzles': [
            {'puzzle_id': None,
             'completed': False,
             'difficulty': 0.5,
             'point_value': 90,
             'pieces': [],
             'players': [{'id': None, 'first_name': 'Sally',
                          'last_name': 'Sue', 'email': 'sallysue@emails.com'}]}
        ]
    }
    assert result == expected


def test_get_sudoku_puzzles_create_one_known_exception(monkeypatch, user):
    class MockParser:
        def add_argument(self, *args, **kwargs):
            pass

        def parse_args(self):
            return {
                'difficulty': 0.5,
                'size': 5
            }

    def mock_save(*args, **kwargs):
        return None

    def raise_exception(*args, **kwargs):
        raise PuzzleException("A bad exception!")

    monkeypatch.setattr(Puzzle, 'save', mock_save)
    monkeypatch.setattr(Puzzle, 'set_pieces', lambda x: None)   # to speed up tests
    monkeypatch.setattr(PuzzlePlayer, 'save', raise_exception)

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        puzzles_resource.parser = MockParser()
        result = puzzles_resource.post()

    expected = ({'message': 'Failed to create new Sudoku Puzzle',
                 'reason': "A bad exception!"}, 400)
    assert result == expected


def test_get_sudoku_puzzles_create_one_unknown_exception(monkeypatch, user):
    class MockParser:
        def add_argument(self, *args, **kwargs):
            pass

        def parse_args(self):
            return {
                'difficulty': 0.5,
                'size': 5
            }

    def mock_save(*args, **kwargs):
        return None

    def raise_exception(*args, **kwargs):
        raise Exception("A generic bad exception!")

    monkeypatch.setattr(Puzzle, 'save', mock_save)
    monkeypatch.setattr(Puzzle, 'set_pieces', lambda x: None)   # to speed up tests
    monkeypatch.setattr(PuzzlePlayer, 'save', raise_exception)

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        puzzles_resource.parser = MockParser()
        result = puzzles_resource.post()

    expected = ({'message': 'Failed to create new Sudoku Puzzle'}, 500)
    assert result == expected


def test_get_sudoku_puzzles_create_one(monkeypatch, user):

    class MockParser:
        def add_argument(self, *args, **kwargs):
            pass

        def parse_args(self):
            return {
                'difficulty': 0.5,
                'size': 5
            }

    def mock_save(*args, **kwargs):
        return None

    def mock_return_id(*args, **kwargs):
        return 1

    monkeypatch.setattr(Puzzle, 'save', mock_return_id)
    monkeypatch.setattr(Puzzle, 'set_pieces', lambda x: None)  # to speed up tests
    monkeypatch.setattr(PuzzlePlayer, 'save', mock_save)
    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        puzzles_resource.parser = MockParser()
        result = puzzles_resource.post()

    expected = {
        'message': 'New Sudoku puzzle successfully created',
        'difficulty': 0.5,
        'size': 5,
        'puzzle_id': 1
    }
    assert result == expected


def test_get_sudoku_puzzle_none_retrieved(monkeypatch, mock_no_puzzles_for_player, user):

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        g.user = user
        result = puzzles_resource.get(1)

    expected = ({'message': f'Puzzle requested does not exist or is '
                            f'not associated with user Jane Doe (id = 1)'}, 404)
    assert result == expected


def test_get_sudoku_puzzle_none_associated(monkeypatch, user):

    def mock_get_puzzles_for_player(*args, **kwargs):
        return [PuzzlePlayer(3, 2)]

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        g.user = user
        result = puzzles_resource.get(1)

    expected = ({'message': f'Puzzle requested does not exist or is '
                            f'not associated with user Jane Doe (id = 1)'}, 404)
    assert result == expected


def test_get_sudoku_puzzle_found(monkeypatch, mock_get_puzzle, user):

    def mock_get_puzzles_for_player(*args, **kwargs):
        return [PuzzlePlayer(1, 1)]

    def mock_get_players(*args, **kwargs):
        user = User(first_name='Sally', last_name='Sue', email='sallysue@emails.com', g_id='123445')
        user.id = 1
        return [user]

    monkeypatch.setattr(PuzzlePlayer, 'find_players_for_puzzle', mock_get_players)
    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        g.user = user
        result = puzzles_resource.get(1)

    expected = {
        'puzzle_id': None,
        'completed': False,
        'difficulty': 0.5,
        'point_value': 90,
        'pieces': [],
        'players': [{'id': 1, 'first_name': 'Sally', 'last_name': 'Sue', 'email': 'sallysue@emails.com'}]
    }
    assert result == expected


def test_join_sudoku_puzzle_already_joined(monkeypatch, user):

    def mock_get_puzzles_for_player(*args, **kwargs):
        return [PuzzlePlayer(1, 1)]

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        g.user = user
        result = puzzles_resource.post(1)

    expected = {'message': "Jane Doe (id = 1) is already is associated with puzzle 1."}
    assert result == expected


def test_join_sudoku_puzzle(monkeypatch, user):

    def mock_get_puzzles_for_player(*args, **kwargs):
        return []

    def mock_add_player(*args, **kwargs):
        return None

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)
    monkeypatch.setattr(PuzzlePlayer, 'add_player_to_puzzle', mock_add_player)

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        g.user = user
        result = puzzles_resource.post(1)

    expected = {'message': "Successfully added Jane Doe (id = 1) to puzzle with id 1."}
    assert result == expected


def test_join_sudoku_puzzle_known_exception(monkeypatch, user):

    def mock_get_puzzles_for_player(*args, **kwargs):
        return []

    def mock_add_player(*args, **kwargs):
        raise PuzzleException("A bad but known exception!")

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)
    monkeypatch.setattr(PuzzlePlayer, 'add_player_to_puzzle', mock_add_player)

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        g.user = user
        result = puzzles_resource.post(1)

    expected = ({'message': 'Attempt to add Jane Doe (id = 1) to puzzle 1 failed.',
                 'reason': 'A bad but known exception!'}, 400)
    assert result == expected


def test_join_sudoku_puzzle_unknown_exception(monkeypatch, user):

    def mock_get_puzzles_for_player(*args, **kwargs):
        return []

    def mock_add_player(*args, **kwargs):
        raise Exception("A very bad exception!")

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)
    monkeypatch.setattr(PuzzlePlayer, 'add_player_to_puzzle', mock_add_player)

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        g.user = user
        result = puzzles_resource.post(1)

    expected = ({'message': 'Attempt to add Jane Doe (id = 1) to puzzle 1 failed.',
                 'reason': 'Unknown error occurred.'}, 500)
    assert result == expected
