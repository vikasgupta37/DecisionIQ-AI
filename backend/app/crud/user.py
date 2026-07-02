from typing import Any, Dict, Optional, Union
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.core.security import get_password_hash, verify_password
from backend.app.models.user import User, UserRole
from backend.app.schemas.user import UserCreate, UserOAuthCreate, UserUpdate


class UserRepository:
    def get(self, db: Session, user_id: int) -> Optional[User]:
        """Retrieves a user by their unique primary key ID"""
        return db.get(User, user_id)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Retrieves a user by their email address"""
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()

    def get_by_google_id(self, db: Session, google_id: str) -> Optional[User]:
        """Retrieves a user by their Google OAuth ID"""
        stmt = select(User).where(User.google_id == google_id)
        return db.execute(stmt).scalar_one_or_none()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Creates a new standard user with a hashed password"""
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            role=obj_in.role,
            is_active=obj_in.is_active,
            avatar_url=obj_in.avatar_url,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_oauth(self, db: Session, *, obj_in: UserOAuthCreate) -> User:
        """Creates a new user registered via Google OAuth"""
        db_obj = User(
            email=obj_in.email,
            google_id=obj_in.google_id,
            full_name=obj_in.full_name,
            role=obj_in.role,
            avatar_url=obj_in.avatar_url,
            hashed_password=None,  # OAuth users have no password initially
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """Updates a user's properties, automatically hashing password if updated"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            db_obj.hashed_password = hashed_password
            del update_data["password"]

        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticates a user by email and password"""
        user = self.get_by_email(db, email=email)
        if not user or not user.hashed_password:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user_repository = UserRepository()
