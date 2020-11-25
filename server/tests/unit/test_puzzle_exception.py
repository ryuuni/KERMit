"""
Unit tests for the Puzzle Exception class.
"""
from backend.models.puzzle_exception import PuzzleException


def test_get_message():
    """
    Test get puzzle exception message.
    """
    msg = "This is a test exception"
    exception = PuzzleException(msg)
    assert exception.get_message() == msg
