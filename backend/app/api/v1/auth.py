from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app.core.config import settings
from backend.app.core.exceptions import DecisionIQException, CredentialsException, DuplicateEntityException
from backend.app.core.security import create_access_token
from backend.app.crud.user import user_repository
from backend.app.models.user import User, UserRole
from backend.app.schemas.user import UserCreate, UserOAuthCreate, UserResponse, Token, GoogleLoginRequest

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Registers a new user in the system with email, name, password and default role.
    """
    user = user_repository.get_by_email(db, email=user_in.email)
    if user:
        raise DuplicateEntityException("User", "email", user_in.email)
    
    new_user = user_repository.create(db, obj_in=user_in)
    return new_user


@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, retrieve a JWT access token using email and password.
    """
    user = user_repository.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise CredentialsException("Incorrect email or password")
    elif not user.is_active:
        raise CredentialsException("Inactive user account")
        
    return Token(
        access_token=create_access_token(subject=user.id),
        token_type="bearer",
    )


@router.post("/google-login", response_model=Token)
def login_with_google(
    *,
    db: Session = Depends(deps.get_db),
    login_data: GoogleLoginRequest,
) -> Any:
    """
    Login or register automatically using a Google OAuth ID token.
    Uses Google OAuth SDK to verify token. Supports mock tokens for testing.
    """
    email = None
    name = None
    picture = None
    google_id = None

    # Production verification using Google libraries
    if settings.GOOGLE_CLIENT_ID:
        try:
            idinfo = id_token.verify_oauth2_token(
                login_data.id_token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            email = idinfo.get("email")
            name = idinfo.get("name")
            picture = idinfo.get("picture")
            google_id = idinfo.get("sub")
            if not email or not google_id:
                raise CredentialsException("Google token is missing email or sub fields")
        except Exception as e:
            raise CredentialsException(f"Invalid Google ID Token: {str(e)}")
    else:
        # Development / Test mock OAuth validation logic
        if login_data.id_token.startswith("mock_"):
            username = login_data.id_token.replace("mock_", "")
            email = f"{username}@example.com"
            name = username.replace("_", " ").title()
            picture = f"http://example.com/avatar/{username}.png"
            google_id = f"google_id_{username}"
        else:
            raise DecisionIQException(
                message="Google OAuth credentials are not configured on this server, and token is not a development mock token.",
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                code="NOT_CONFIGURED"
            )

    # Check if user already exists by google_id or email
    user = user_repository.get_by_google_id(db, google_id=google_id)
    if not user:
        # If user doesn't exist by google_id, check by email
        user = user_repository.get_by_email(db, email=email)
        if user:
            # Link Google ID to existing password user
            user = user_repository.update(db, db_obj=user, obj_in={"google_id": google_id, "avatar_url": picture})
        else:
            # Create a brand new Google user
            oauth_in = UserOAuthCreate(
                email=email,
                full_name=name,
                google_id=google_id,
                avatar_url=picture,
                role=UserRole.BUSINESS_USER
            )
            user = user_repository.create_oauth(db, obj_in=oauth_in)

    if not user.is_active:
        raise CredentialsException("Inactive user account")

    return Token(
        access_token=create_access_token(subject=user.id),
        token_type="bearer",
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Returns the profile information of the currently logged-in user.
    """
    return current_user
