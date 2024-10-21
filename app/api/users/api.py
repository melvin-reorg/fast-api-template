"""This module contains the API endpoints for the example module."""

from fastapi import APIRouter, Depends

from app.utils.dependencies import get_db
from .services import UserService
from sqlalchemy.orm import Session


from .schemas import User, UserCreate, UserUpdate

router = APIRouter()
PATH = "/users"
DETAIL_PATH = "/user/{user_id}"


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post(PATH, response_model=User, summary="Create a new user")
async def create_user(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
) -> User:
    created_user = user_service.create_user(user)
    return created_user


@router.get(PATH, response_model=list[User], summary="Get all users")
async def get_users(
    user_service: UserService = Depends(get_user_service),
) -> list[User]:
    users = user_service.get_users()
    return users


@router.get(DETAIL_PATH, response_model=User, summary="Get a user by ID")
async def get_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
) -> User:
    user = user_service.get_user(user_id)
    return user


@router.put(DETAIL_PATH, response_model=UserUpdate, summary="Update a user by ID")
async def update_user(
    user_id: int,
    user: UserUpdate,
    user_service: UserService = Depends(get_user_service),
) -> User:
    updated_user = user_service.update_user(user_id, user)
    return updated_user


@router.delete(DETAIL_PATH, response_model=dict, summary="Delete a user by ID")
async def delete_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
) -> dict:
    deleted_user = user_service.delete_user(user_id)
    return deleted_user
