from server.server import app                    # this dependency is necessary to prevent a circular import
from server.models.sudoku_puzzle import Puzzle
from server.models.puzzle_exception import PuzzleException
from server.config import UnitTestingConfig
import pytest

app.config.from_object(UnitTestingConfig)


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

