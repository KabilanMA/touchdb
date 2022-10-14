
class CustomError(Exception):
    """Base class for custom exceptions"""
    pass


class NoValueError(CustomError):
    """Raise when no value is provided to insert into the database"""
    pass