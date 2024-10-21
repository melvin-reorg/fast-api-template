from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from .models import Todo as TodoModel

from .schemas import TodoCreate, Todo, TodoUpdate


class TodoService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_todo(self, todo_in: TodoCreate, user_id: int) -> Todo:
        try:
            todo = TodoModel(
                title=todo_in.title,
                description=todo_in.description,
                done=todo_in.done,
                user_id=user_id,
            )
            self.db.add(todo)
            self.db.commit()
            self.db.refresh(todo)
            return todo
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating todo: {e}",
            )

    def get_todos(self, skip: int = 0, limit: int = 10) -> [Todo]:
        todos = self.db.query(TodoModel).offset(skip).limit(limit).all()
        return [Todo.model_validate(todo) for todo in todos]

    def get_todo_by_id(self, todo_id: int, user_id: int) -> Todo:
        todo = (
            self.db.query(TodoModel)
            .filter(TodoModel.id == todo_id, TodoModel.user_id == user_id)
            .first()
        )
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return Todo.model_validate(todo)

    def get_todo_by_user_id(self, user_id: int) -> [Todo]:
        todos = self.db.query(TodoModel).filter(TodoModel.user_id == user_id).all()
        return [Todo.model_validate(todo) for todo in todos]

    def update_todo(self, todo_id: int, todo_in: TodoUpdate, user_id: int) -> Todo:
        todo = (
            self.db.query(TodoModel)
            .filter(TodoModel.id == todo_id, TodoModel.user_id == user_id)
            .first()
        )
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )

        todo.title = todo_in.title or todo.title
        todo.description = todo_in.description or todo.description
        todo.done = todo_in.done or todo.done

        self.db.commit()
        self.db.refresh(todo)
        return Todo.model_validate(todo)

    def delete_todo(self, todo_id: int, user_id: int) -> dict:
        todo = (
            self.db.query(TodoModel)
            .filter(TodoModel.id == todo_id, TodoModel.user_id == user_id)
            .first()
        )
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        self.db.delete(todo)
        self.db.commit()
        return {"detail": "Todo deleted successfully"}
