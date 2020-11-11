import pytest
from server.server import app, db
from server.config import UnitTestingConfig
from server.models.puzzle_exception import PuzzleException
from server.models.puzzle_pieces import PuzzlePiece
from server.tests.unit.mock_session import MockSession

app.config.from_object(UnitTestingConfig)


@pytest.fixture
def puzzle_piece():
    test_puzzle_piece = PuzzlePiece(1, 0, 0, value=7, static_piece=False)
    test_puzzle_piece.id = 1
    return test_puzzle_piece


def test_find_all_pieces(monkeypatch, puzzle_piece):
    class MockBaseQuery:
        def __init__(self, *args, **kwargs):
            pass

        def filter_by(self, *args, **kwargs):
            class Results():
                def all(self):
                    return [puzzle_piece]

            return Results()

        def join(self, *args, **kwargs):
            return

    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    result = PuzzlePiece.find_all_pieces(1)
    expected = [puzzle_piece]
    assert expected == result


def test_get_piece(monkeypatch, puzzle_piece):
    class MockBaseQuery:

        def __init__(self, *args, **kwargs):
            pass

        def filter_by(self, *args, **kwargs):
            class Results():
                def first(self):
                    return puzzle_piece

            return Results()

        def join(self, *args, **kwargs):
            return

    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    result = PuzzlePiece.get_piece(1, 0, 0)
    expected = puzzle_piece
    assert expected == result


def test_get_piece_none(monkeypatch):
    class MockBaseQuery:

        def __init__(self, *args, **kwargs):
            pass

        def filter_by(self, *args, **kwargs):
            class Results():
                def first(self):
                    return None

            return Results()

        def join(self, *args, **kwargs):
            return

    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    with pytest.raises(PuzzleException) as pe:
        result = PuzzlePiece.get_piece(1, 100, -1)


def test_save_autocommit(monkeypatch, puzzle_piece):
    monkeypatch.setattr(db, "session", MockSession)

    puzzle_piece.save(autocommit=True)
    assert True


def test_save(monkeypatch, puzzle_piece):
    monkeypatch.setattr(db, "session", MockSession)

    puzzle_piece.save(autocommit=False)
    assert True  # just want to make sure we can get here


def test_update_success(monkeypatch, puzzle_piece):
    monkeypatch.setattr(db, "session", MockSession)

    puzzle_piece.update(5, autocommit=True)
    assert puzzle_piece.value == 5


def test_update_fail_static(monkeypatch):
    monkeypatch.setattr(db, "session", MockSession)

    piece = PuzzlePiece(1, 0, 0, value=7, static_piece=True)
    with pytest.raises(PuzzleException) as pe:
        piece.update(5, autocommit=True)


def test_get_as_str(puzzle_piece):
    assert str(puzzle_piece) == 'PuzzlePiece(id=1, puzzle_id=1, x_coordinate=0, ' \
                                'y_coordinate=0, value=7, static_piece=False)'
