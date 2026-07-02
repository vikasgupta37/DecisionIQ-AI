from typing import Generator, List
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.core.exceptions import CredentialsException, PermissionDeniedException
from backend.app.core.security import decode_access_token
from backend.app.crud.user import user_repository
from backend.app.models.user import User, UserRole
from backend.app.schemas.user import TokenPayload

# Setup reusable oauth2 scheme
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    """
    Dependency injection function to extract and validate 
    the active logged-in user from the JWT request header.
    """
    try:
        payload = decode_access_token(token)
        token_data = TokenPayload(**payload)
        if not token_data.sub:
            raise CredentialsException()
    except (jwt.PyJWTError, ValueError):
        raise CredentialsException()
    
    # Retrieve user from DB. The subject is stored as user ID string in token
    try:
        user_id = int(token_data.sub)
    except ValueError:
        raise CredentialsException("Invalid user subject in token")
        
    user = user_repository.get(db, user_id=user_id)
    if not user:
        raise CredentialsException("User associated with token does not exist")
    if not user.is_active:
        raise PermissionDeniedException("User account is inactive")
        
    return user


class RoleChecker:
    """
    Dependency class to enforce Role-Based Access Control (RBAC) on endpoints.
    Allows specifying one or more roles that are authorized.
    """
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise PermissionDeniedException(
                f"Requires one of the following roles: {[r.value for r in self.allowed_roles]}"
            )
        return current_user
