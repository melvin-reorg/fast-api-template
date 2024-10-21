"""
Pydantic schemas for Todo model
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    done: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    done: Optional[bool] = None


class TodoInDBBase(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class Todo(TodoInDBBase):
    pass


class TodoInDB(TodoInDBBase):
    pass
