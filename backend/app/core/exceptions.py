from typing import Any, Dict, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.requests import Request


class DecisionIQException(Exception):
    """Base exception class for DecisionIQ AI Platform"""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: str = "BAD_REQUEST",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or {}


class CredentialsException(DecisionIQException):
    """Exception raised when credential authentication fails"""
    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="UNAUTHORIZED",
            details={"headers": {"WWW-Authenticate": "Bearer"}},
        )


class PermissionDeniedException(DecisionIQException):
    """Exception raised when authorization RBAC checks fail"""
    def __init__(self, message: str = "Permission denied. Insufficient role permissions."):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
        )


class EntityNotFoundException(DecisionIQException):
    """Exception raised when requested resource is missing"""
    def __init__(self, entity_name: str, identifier: Any):
        super().__init__(
            message=f"{entity_name} with identifier '{identifier}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
        )


class DuplicateEntityException(DecisionIQException):
    """Exception raised when creating an entity that already exists"""
    def __init__(self, entity_name: str, field: str, value: Any):
        super().__init__(
            message=f"{entity_name} with {field} '{value}' already exists.",
            status_code=status.HTTP_409_CONFLICT,
            code="CONFLICT",
        )


def setup_exception_handlers(app: FastAPI) -> None:
    """Sets up custom exception handlers on the FastAPI application"""
    
    @app.exception_handler(DecisionIQException)
    async def decisioniq_exception_handler(request: Request, exc: DecisionIQException):
        content = {
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
        headers = exc.details.get("headers") if isinstance(exc.details, dict) else None
        return JSONResponse(
            status_code=exc.status_code,
            content=content,
            headers=headers,
        )

    @app.exception_handler(HTTPException)
    async def fastapi_http_exception_handler(request: Request, exc: HTTPException):
        content = {
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
                "details": {}
            }
        }
        return JSONResponse(
            status_code=exc.status_code,
            content=content,
        )
