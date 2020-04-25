class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class WrongAttributeError(Error):
    pass


class WrongValueError(Error):
    pass
