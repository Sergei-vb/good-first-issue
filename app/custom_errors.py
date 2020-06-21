class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class WrongAttrError(Error):
    pass


class WrongValueError(Error):
    pass


class WrongResponse(Error):
    pass
