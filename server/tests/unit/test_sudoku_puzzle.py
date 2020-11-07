from server.server import app                    # this dependency is necessary to prevent a circular import
from server.models.sudoku_puzzle import Puzzle
from server.models.puzzle_pieces import PuzzlePiece
from server.models.puzzle_exception import PuzzleException
from server.config import UnitTestingConfig
import pytest

app.config.from_object(UnitTestingConfig)


@pytest.fixture(autouse=False)
def incomplete_puzzle():
    """
    Have an incomplete puzzle that can be used for testing
    """
    puzzle = Puzzle(difficulty_level=0.2, size=2)
    puzzle.id = 1
    puzzle.puzzle_pieces = [
        PuzzlePiece(1, 0, 0, value=2, static_piece=True),
        PuzzlePiece(1, 1, 0, value=4, static_piece=True),
        PuzzlePiece(1, 2, 0, value=3, static_piece=True),
        PuzzlePiece(1, 3, 0, value=1, static_piece=True),
        PuzzlePiece(1, 0, 1, value=1, static_piece=True),
        PuzzlePiece(1, 1, 1, value=3, static_piece=False),
        PuzzlePiece(1, 2, 1, value=4, static_piece=True),
        PuzzlePiece(1, 3, 1, value=2, static_piece=True),
        PuzzlePiece(1, 0, 2, value=None, static_piece=False),
        PuzzlePiece(1, 1, 2, value=2, static_piece=True),
        PuzzlePiece(1, 2, 2, value=1, static_piece=True),
        PuzzlePiece(1, 3, 2, value=3, static_piece=True),
        PuzzlePiece(1, 0, 3, value=3, static_piece=True),
        PuzzlePiece(1, 1, 3, value=1, static_piece=True),
        PuzzlePiece(1, 2, 3, value=None, static_piece=False),
        PuzzlePiece(1, 3, 3, value=4, static_piece=True)
    ]
    return puzzle


@pytest.fixture(autouse=False)
def complete_puzzle():
    puzzle = Puzzle(difficulty_level=0.2, size=2)
    puzzle.id = 1
    puzzle.puzzle_pieces = [
        PuzzlePiece(1, 0, 0, value=2, static_piece=True),
        PuzzlePiece(1, 1, 0, value=4, static_piece=True),
        PuzzlePiece(1, 2, 0, value=3, static_piece=True),
        PuzzlePiece(1, 3, 0, value=1, static_piece=True),
        PuzzlePiece(1, 0, 1, value=1, static_piece=True),
        PuzzlePiece(1, 1, 1, value=3, static_piece=False),
        PuzzlePiece(1, 2, 1, value=4, static_piece=True),
        PuzzlePiece(1, 3, 1, value=2, static_piece=True),
        PuzzlePiece(1, 0, 2, value=4, static_piece=False),
        PuzzlePiece(1, 1, 2, value=2, static_piece=True),
        PuzzlePiece(1, 2, 2, value=1, static_piece=True),
        PuzzlePiece(1, 3, 2, value=3, static_piece=True),
        PuzzlePiece(1, 0, 3, value=3, static_piece=True),
        PuzzlePiece(1, 1, 3, value=1, static_piece=True),
        PuzzlePiece(1, 2, 3, value=2, static_piece=False),
        PuzzlePiece(1, 3, 3, value=4, static_piece=True)
    ]
    return puzzle


@pytest.fixture(autouse=False)
def incorrect_puzzle():
    puzzle = Puzzle(difficulty_level=0.2, size=2)
    puzzle.id = 1
    puzzle.puzzle_pieces = [
        PuzzlePiece(1, 0, 0, value=2, static_piece=True),
        PuzzlePiece(1, 1, 0, value=4, static_piece=True),
        PuzzlePiece(1, 2, 0, value=3, static_piece=True),
        PuzzlePiece(1, 3, 0, value=1, static_piece=True),
        PuzzlePiece(1, 0, 1, value=1, static_piece=True),
        PuzzlePiece(1, 1, 1, value=1, static_piece=False),
        PuzzlePiece(1, 2, 1, value=4, static_piece=True),
        PuzzlePiece(1, 3, 1, value=2, static_piece=True),
        PuzzlePiece(1, 0, 2, value=2, static_piece=False),
        PuzzlePiece(1, 1, 2, value=2, static_piece=True),
        PuzzlePiece(1, 2, 2, value=1, static_piece=True),
        PuzzlePiece(1, 3, 2, value=3, static_piece=True),
        PuzzlePiece(1, 0, 3, value=3, static_piece=True),
        PuzzlePiece(1, 1, 3, value=1, static_piece=True),
        PuzzlePiece(1, 2, 3, value=4, static_piece=False),
        PuzzlePiece(1, 3, 3, value=4, static_piece=True)
    ]
    return puzzle


def test_create_sudoku_puzzle_valid_defaults():
    """
    Make sure that it is possible to create a sudoku puzzle using defaults.
    """
    sudoku = Puzzle()
    assert sudoku.difficulty == 0.5
    assert sudoku.size == 3
    assert not sudoku.completed


def test_create_sudoku_puzzle_valid_specification():
    """
    Make sure that it is possible to create a sudoku puzzle by specifying difficulty and size.
    """
    sudoku = Puzzle(difficulty_level=0.6, size=4)
    assert sudoku.difficulty == 0.6
    assert sudoku.size == 4
    assert not sudoku.completed


def test_create_sudoku_puzzle_invalid_difficulty_str():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid difficulty level
    that is not of type float.
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level='bad level', size=4)
        assert "Sudoku puzzle difficulty specified must be a float value" in str(pe.value)


def test_create_sudoku_puzzle_invalid_difficulty_too_low():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid difficulty level
    that is out of range (too low).
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level=0.0, size=4)
        assert "Difficulty levels must range between" in str(pe.value)


def test_create_sudoku_puzzle_invalid_difficulty_too_high():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid difficulty level
    that is out of range (too high).
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level=1.1, size=4)
        assert "Difficulty levels must range between" in str(pe.value)


def test_create_sudoku_puzzle_invalid_size_str():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid size
    that is not of type int.
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level='bad size', size=4)
        assert "Sudoku puzzle sizes specified must be valid integers" in str(pe.value)


def test_create_sudoku_puzzle_invalid_size_too_low():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid size
    that is out of range (too low).
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level=0.5, size=0)
        assert "Valid sizes range from" in str(pe.value)


def test_create_sudoku_puzzle_invalid_size_too_high():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid size
    that is out of range (too high).
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level=0.5, size=10)
        assert "Valid sizes range from" in str(pe.value)


def test_set_point_value1():
    """
    Make sure that point values are calculated correctly based on difficulty and size.
    """
    sudoku = Puzzle(difficulty_level=0.6, size=4)
    assert sudoku.point_value == 110


def test_set_point_value2():
    """
    Make sure that point values are calculated correctly based on difficulty and size.
    """
    sudoku = Puzzle(difficulty_level=0.2, size=3)
    assert sudoku.point_value == 50


def test_get_pieces_as_arr_all(incomplete_puzzle):
    """
    Test get the pieces as an array of values for testing
    """
    result = incomplete_puzzle.get_pieces_as_arr(static_only=False)
    expected = [[2, 4, 3, 1], [1, 3, 4, 2], [None, 2, 1, 3], [3, 1, None, 4]]
    assert result == expected


def test_get_pieces_as_arr_static_only(incomplete_puzzle):
    """
    Test get the pieces as an array of values for testing; this should be the original
    puzzle board ONLY
    """
    result = incomplete_puzzle.get_pieces_as_arr(static_only=True)
    expected = [[2, 4, 3, 1], [1, None, 4, 2], [None, 2, 1, 3], [3, 1, None, 4]]
    assert result == expected


def test_recreate_original_puzzle(incomplete_puzzle):
    """
    Test get the pieces as an array of values for testing; this should be the original
    puzzle board ONLY
    """
    result = incomplete_puzzle.recreate_original_puzzle_as_array()
    expected = [[2, 4, 3, 1], [1, None, 4, 2], [None, 2, 1, 3], [3, 1, None, 4]]
    assert result == expected


def test_check_for_completion_null_values(incomplete_puzzle):
    """
    A puzzle is not complete if there are pieces in the puzzle with null (i.e., None) values.
    """
    assert not incomplete_puzzle.is_complete_puzzle()


def test_check_for_completion_complete(complete_puzzle):
    """
    A puzzle that is complete should be deemed complete in the completeness check.
    """
    assert complete_puzzle.is_complete_puzzle()


def test_check_for_completion_incorrect_values(incorrect_puzzle):
    """
    A puzzle is not complete if there are pieces that are not valid.
    """
    assert not incorrect_puzzle.is_complete_puzzle()


def test_check_discrepancies_none(complete_puzzle):
    """
    A puzzle is not complete if there are pieces that are not valid.
    """
    assert [] == complete_puzzle.compare_with_solved_board()


def test_check_discrepancies_many_incorrect(incorrect_puzzle):
    """
    A puzzle is not complete if there are pieces that are not valid.
    """
    expected = [
        {'x_coordinate': 1, 'y_coordinate': 1},
        {'x_coordinate': 0, 'y_coordinate': 2},
        {'x_coordinate': 2, 'y_coordinate': 3}
    ]
    assert expected == incorrect_puzzle.compare_with_solved_board()


def test_check_discrepancies_incomplete_puzzle(incomplete_puzzle):
    """
    A puzzle is not complete if there are pieces that are not valid.
    """
    expected = [
        {'x_coordinate': 0, 'y_coordinate': 2},
        {'x_coordinate': 2, 'y_coordinate': 3}
    ]
    assert expected == incomplete_puzzle.compare_with_solved_board()

