from typing import List

from fastapi import APIRouter, Depends

from .schemas import Todo, TodoCreate, TodoUpdate
from .services import TodoService
from app.utils.dependencies import get_db
from sqlalchemy.orm import Session


router = APIRouter()


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    return TodoService(db)


@router.post("/users/{user_id}/todos", response_model=Todo)
def create_todo(
    user_id: int,
    todo: TodoCreate,
    todo_service: TodoService = Depends(get_todo_service),
) -> Todo:
    created_todo = todo_service.create_todo(todo, user_id)
    return created_todo


@router.get("/users/{user_id}/todos", response_model=List[Todo])
def get_todos(
    user_id: int, todo_service: TodoService = Depends(get_todo_service)
) -> List[Todo]:
    todos = todo_service.get_todo_by_user_id(user_id)
    return todos


@router.get("/users/{user_id}/todos/{todo_id}", response_model=Todo)
def get_todo_by_id(
    user_id: int, todo_id: int, todo_service: TodoService = Depends(get_todo_service)
) -> Todo:
    todo = todo_service.get_todo_by_id(todo_id, user_id)
    return todo


@router.put("/users/{user_id}/todos/{todo_id}", response_model=Todo)
def update_todo(
    user_id: int,
    todo_id: int,
    todo: TodoUpdate,
    todo_service: TodoService = Depends(get_todo_service),
) -> Todo:
    updated_todo = todo_service.update_todo(todo_id, todo, user_id)
    return updated_todo


@router.delete("/users/{user_id}/todos/{todo_id}")
def delete_todo(
    user_id: int, todo_id: int, todo_service: TodoService = Depends(get_todo_service)
) -> dict:
    deleted_todo = todo_service.delete_todo(todo_id, user_id)
    return deleted_todo
