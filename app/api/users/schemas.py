"""This module contains the schemas for this example module."""

from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from app.api.todos.schemas import Todo, TodoInDB


class UserBase(BaseModel):
    name: str = Field(..., max_length=100, description="The name of the user")
    email: EmailStr = Field(..., description="The email of the user")


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    todos: List[Todo] = []


class UserInDB(UserInDBBase):
    todos: List[TodoInDB] = []
