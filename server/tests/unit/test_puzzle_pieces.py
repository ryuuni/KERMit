"""
Unit tests for the Puzzle Pieces class.
"""
import pytest
from backend import app, db
from backend.config import UnitTestingConfig
from backend.models.puzzle_exception import PuzzleException
from backend.models.puzzle_pieces import PuzzlePiece
from tests.unit.mock_session import MockSession

app.config.from_object(UnitTestingConfig)


@pytest.fixture
def puzzle_piece():
    """
    Test create puzzle piece.
    """
    test_puzzle_piece = PuzzlePiece(1, 0, 0, value=7, static_piece=False)
    test_puzzle_piece.id = 1
    return test_puzzle_piece


def test_find_all_pieces(monkeypatch, puzzle_piece):
    """
    Test find all puzzle pieces for a given puzzle, mocking the
    base query that finds the pieces.
    """
    class MockBaseQuery:
        """
        Mock the database base query class, so that unit test does not hit actual db
        """
        def __init__(self, *args, **kwargs):
            pass

        def filter_by(self, *args, **kwargs):
            """
            Mock filter by function.
            """
            class Results():
                """
                Mock results class, aims to provide a fake database result for test
                """
                def all(self):
                    """
                    Mock all function, which is supposed to provide all results for a
                    database query.
                    """
                    return [puzzle_piece]

            return Results()

        def join(self, *args, **kwargs):
            """
            Mock join function
            """
            return

    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    result = PuzzlePiece.find_all_pieces(1)
    expected = [puzzle_piece]
    assert expected == result


def test_get_piece(monkeypatch, puzzle_piece):
    """
    Test find an individual piece, mocking the base query that finds the pieces.
    """
    class MockBaseQuery:
        """
        Mock the database base query class, so that unit test does not hit actual db
        """
        def __init__(self, *args, **kwargs):
            pass

        def filter_by(self, *args, **kwargs):
            """
            Mock filter by function.
            """
            class Results():
                """
                Mock results class, aims to provide a fake database result for test
                """
                def first(self):
                    """
                    Mock first function
                    """
                    return puzzle_piece

            return Results()

        def join(self, *args, **kwargs):
            """
            Mock join function, doesn't do anything important.
            """
            return

    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    result = PuzzlePiece.get_piece(1, 0, 0)
    expected = puzzle_piece
    assert expected == result


def test_get_piece_none(monkeypatch):
    """
    Test attempt to find a puzzle piece that doesn't exist.
    """
    class MockBaseQuery:
        """
        Mock the database base query class, so that unit test does not hit actual db
        """
        def __init__(self, *args, **kwargs):
            pass

        def filter_by(self, *args, **kwargs):
            """
            Mock filter by function.
            """
            class Results():
                """
                Mock results class, aims to provide a fake database result for test
                """
                def first(self):
                    """
                    Mock first function
                    """
                    return None

            return Results()

        def join(self, *args, **kwargs):
            """
            Mock join function, doesn't do anything important.
            """
            return

    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    with pytest.raises(PuzzleException):
        PuzzlePiece.get_piece(1, 100, -1)


def test_save_autocommit(monkeypatch, puzzle_piece):
    """
    Test attempt save puzzle piece, with database session mocked, autocommit on.
    """
    monkeypatch.setattr(db, "session", MockSession)

    puzzle_piece.save(autocommit=True)
    assert True


def test_save(monkeypatch, puzzle_piece):
    """
    Test attempt save puzzle piece, with database session mocked, autocommit off.
    """
    monkeypatch.setattr(db, "session", MockSession)

    puzzle_piece.save(autocommit=False)
    assert True  # just want to make sure we can get here


def test_update_success(monkeypatch, puzzle_piece):
    """
    Test attempt update puzzle piece, valid change made to non-static piece.
    """
    monkeypatch.setattr(db, "session", MockSession)

    puzzle_piece.update(5, autocommit=True)
    assert puzzle_piece.value == 5


def test_update_fail_static(monkeypatch):
    """
    Test attempt update puzzle piece, invalid attempt made to static piece.
    """
    monkeypatch.setattr(db, "session", MockSession)

    piece = PuzzlePiece(1, 0, 0, value=7, static_piece=True)
    with pytest.raises(PuzzleException):
        piece.update(5, autocommit=True)


def test_get_as_str(puzzle_piece):
    """
    Test get puzzle piece as a readable string.
    """
    assert str(puzzle_piece) == 'PuzzlePiece(id=1, puzzle_id=1, x_coordinate=0, ' \
                                'y_coordinate=0, value=7, static_piece=False)'
