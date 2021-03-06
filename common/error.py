"""
Contains all exceptions
"""


class EmailAddressInvalid(Exception):
    pass


class UnexpectedAlert(Exception):
    pass


class SheetTypeError(Exception):
    pass


class LocationTypeError(Exception):
    pass


class BrowserNoFoundError(Exception):
    pass


class NotFoundError(Exception):
    pass


class InvalidLocationError(Exception):
    pass


class FileNotFound(FileNotFoundError, NotFoundError):
    pass



