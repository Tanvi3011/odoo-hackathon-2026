from fastapi import HTTPException


class HRMSException(HTTPException):
    pass


class NotFoundException(HRMSException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class ConflictException(HRMSException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(status_code=409, detail=detail)


class ForbiddenException(HRMSException):
    def __init__(self, detail: str = "Access denied"):
        super().__init__(status_code=403, detail=detail)


class UnauthorizedException(HRMSException):
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(status_code=401, detail=detail)


class ValidationException(HRMSException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=422, detail=detail)
