"""
Class to handle exceptions specific to this Sudoku Puzzle project.
"""


class PuzzleException(Exception):
    """
    Exception class capable of accepting a message with issue
    specific to a validation case of this puzzle application.
    """
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def get_message(self):
        """
        Allows the message outlining the source of the exception
        to be readily returned.
        """
        return self.msg
