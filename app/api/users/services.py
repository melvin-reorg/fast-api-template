"""This module contains the services i.e. the functions that interact with the db for this example module."""

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import User as UserModel

from .schemas import User, UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, user_in: UserCreate) -> User:
        try:
            user = UserModel(
                name=user_in.name,
                email=user_in.email,
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return User.model_validate(user)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating user: {e}",
            )

    def get_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        users = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [User.model_validate(user) for user in users]

    def get_user(self, user_id: int) -> User:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return User.model_validate(user)

    def update_user(self, user_id: int, user_in: UserUpdate) -> User:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        user.name = user_in.name or user.name
        user.email = user_in.email or user.email

        self.db.commit()
        self.db.refresh(user)
        return User.model_validate(user)

    def delete_user(self, user_id: int) -> dict:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        self.db.delete(user)
        self.db.commit()
        return {"detail": "User deleted successfully"}
