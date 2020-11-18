"""
Mock Session class for testing.
"""


class MockSession:
    """
    A class to provide easy mocking for sqlalchemy database sessions during testing.
    """
    def __init__(self, *args, **kwargs):
        self.value = None
        self.args = args
        self.kwargs = kwargs

    def add(self):
        """
        Mock add method
        """
        return

    @staticmethod
    def commit():
        """
        Mock commit method
        """
        return

    @staticmethod
    def flush():
        """
        Mock flush method
        """
        return

    @staticmethod
    def remove():
        """
        Mock remove method
        """
        return
