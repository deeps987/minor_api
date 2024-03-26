from dataclasses import dataclass
class CustomException(Exception):
    def __init__(self, code=500, error="InternalServerError", message="Server Problem"):
        self.code = code
        self.error = error
        self.message = message

class DBException(CustomException):
    pass
#

class DoesNotExist(CustomException):
    pass

class InvalidCredentials(CustomException):
    pass

class AlreadyExists(CustomException):
    pass

class Error(CustomException):
    pass

class InvalidParams(CustomException):
    pass

class InternalError(CustomException):
    pass

class RoleError(CustomException):
    pass

class BadInput(CustomException):
    pass

class NotFound(CustomException):
    pass
    # def __init__(self):
        # super().__init__()

class IntegrityError(DBException):
    pass

