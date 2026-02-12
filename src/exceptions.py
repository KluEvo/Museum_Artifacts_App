class AppErrorException(Exception):
    status_code = 500

    def __init__(self, message: str):
        super().__init__(message)


class ValidationException(AppErrorException):
    status_code = 400


class NotFoundException(AppErrorException):
    status_code = 404


class PermissionDeniedException(AppErrorException):
    status_code = 403


class ConflictException(AppErrorException):
    status_code = 409
