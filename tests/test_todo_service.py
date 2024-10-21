import pytest

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from app.api.todos.services import TodoService
from app.api.users.services import UserService
from app.api.users.schemas import UserCreate
from app.api.todos.schemas import TodoCreate, TodoUpdate
from app.utils.common import unique_email

USER_NAME = "Pancho"


def test_create_todo_for_user(db_session):
    """
    Test the creation of a todo item for a user.

    Args:
        db_session: The database session fixture.

    Asserts:
        - The created todo has a non-null id.
        - The created todo has the expected title, description, and done status.
        - The created todo is associated with the correct user.
    """
    user_service = UserService(db_session)
    todo_service = TodoService(db_session)

    # Create a user to associate with the todo
    user_in = UserCreate(name=USER_NAME, email=unique_email())
    user = user_service.create_user(user_in)

    # Create a todo for the user
    todo_in = TodoCreate(
        title="Test Todo", description="This is a test todo", done=False
    )
    todo = todo_service.create_todo(todo_in, user.id)

    assert todo.id is not None
    assert todo.title == "Test Todo"
    assert todo.description == "This is a test todo"
    assert todo.done is False
    assert todo.user_id == user.id


def test_get_todo_by_id(db_session):
    """
    Test retrieving a todo item by its id.

    Args:
        db_session: The database session fixture.

    Asserts:
        - The retrieved todo has the expected id, title, description, done status, and user id.
    """
    user_service = UserService(db_session)
    todo_service = TodoService(db_session)

    # Create a user to associate with the todo
    user_in = UserCreate(name=USER_NAME, email=unique_email())
    user = user_service.create_user(user_in)

    # Create a todo for the user
    todo_in = TodoCreate(title="Todo 1", description="First todo", done=False)
    created_todo = todo_service.create_todo(todo_in, user.id)

    # Retrieve the todo by id
    todo = todo_service.get_todo_by_id(created_todo.id, user.id)

    assert todo.id == created_todo.id
    assert todo.title == "Todo 1"
    assert todo.description == "First todo"
    assert todo.done is False
    assert todo.user_id == user.id


def test_get_todos_for_user(db_session):
    """
    Test retrieving all todo items for a user.

    Args:
        db_session: The database session fixture.

    Asserts:
        - The number of retrieved todos is correct.
        - The titles of the retrieved todos are as expected.
    """
    user_service = UserService(db_session)
    todo_service = TodoService(db_session)

    # Create a user to associate with the todos
    user_in = UserCreate(name=USER_NAME, email=unique_email())
    user = user_service.create_user(user_in)

    # Create multiple todos for the user
    todo_in1 = TodoCreate(title="Todo 1", description="First todo", done=False)
    todo_in2 = TodoCreate(title="Todo 2", description="Second todo", done=False)
    todo_service.create_todo(todo_in1, user.id)
    todo_service.create_todo(todo_in2, user.id)

    # Retrieve todos for the user
    todos = todo_service.get_todo_by_user_id(user.id)

    assert len(todos) == 2
    assert todos[0].title == "Todo 1"
    assert todos[1].title == "Todo 2"


def test_update_todo(db_session):
    """
    Test updating a todo item.

    Args:
        db_session: The database session fixture.

    Asserts:
        - The updated todo has the expected id, title, description, and done status.
    """
    user_service = UserService(db_session)
    todo_service = TodoService(db_session)

    # Create a user to associate with the todo
    user_in = UserCreate(name=USER_NAME, email=unique_email())
    user = user_service.create_user(user_in)

    # Create a todo for the user
    todo_in = TodoCreate(title="Todo 1", description="First todo", done=False)
    created_todo = todo_service.create_todo(todo_in, user.id)

    # Update the todo
    todo_update = TodoUpdate(
        title="Updated Todo", description="Updated description", done=True
    )
    updated_todo = todo_service.update_todo(created_todo.id, todo_update, user.id)

    assert updated_todo.id == created_todo.id
    assert updated_todo.title == "Updated Todo"
    assert updated_todo.description == "Updated description"
    assert updated_todo.done is True


def test_delete_todo(db_session):
    """
    Test deleting a todo item.

    Args:
        db_session: The database session fixture.

    Asserts:
        - The response indicates successful deletion.
        - The todo no longer exists in the database.
    """
    user_service = UserService(db_session)
    todo_service = TodoService(db_session)

    # Create a user to associate with the todo
    user_in = UserCreate(name=USER_NAME, email=unique_email())
    user = user_service.create_user(user_in)

    # Create a todo for the user
    todo_in = TodoCreate(title="Todo 1", description="First todo", done=False)
    created_todo = todo_service.create_todo(todo_in, user.id)

    # Delete the todo
    response = todo_service.delete_todo(created_todo.id, user.id)

    assert response == {"detail": "Todo deleted successfully"}

    # Ensure the todo no longer exists
    with pytest.raises(Exception) as e:
        todo_service.get_todo_by_id(created_todo.id, user.id)
    assert "Todo not found" in str(e.value)


def test_create_todo_failure(db_session, mocker):
    """
    Test failure to create a todo item due to a simulated database error.

    Args:
        db_session: The database session fixture.
        mocker: The mocker fixture for mocking objects.

    Asserts:
        - An HTTPException is raised with the expected status code and detail message.
    """
    user_service = UserService(db_session)
    todo_service = TodoService(db_session)

    user_in = UserCreate(name=USER_NAME, email=unique_email())
    user = user_service.create_user(user_in)

    todo_in = TodoCreate(
        title="Test Todo", description="This is a test todo", done=False
    )

    mocker.patch.object(
        db_session, "add", side_effect=SQLAlchemyError("Simulated database error")
    )

    with pytest.raises(HTTPException) as exc_info:
        todo_service.create_todo(todo_in, user.id)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Error creating todo" in exc_info.value.detail


def test_get_todo_not_found(db_session):
    """
    Test retrieving a non-existent todo item.

    Args:
        db_session: The database session fixture.

    Asserts:
        - An HTTPException is raised with the expected status code and detail message.
    """
    user_service = UserService(db_session)
    todo_service = TodoService(db_session)

    user_in = UserCreate(name=USER_NAME, email=unique_email())
    user = user_service.create_user(user_in)

    non_existent_todo_id = 999

    with pytest.raises(HTTPException) as exc_info:
        todo_service.get_todo_by_id(non_existent_todo_id, user.id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Todo not found"


def test_update_todo_not_found(db_session):
    """
    Test updating a non-existent todo item.

    Args:
        db_session: The database session fixture.

    Asserts:
        - An HTTPException is raised with the expected status code and detail message.
    """
    user_service = UserService(db_session)
    todo_service = TodoService(db_session)

    user_in = UserCreate(name=USER_NAME, email=unique_email())
    user = user_service.create_user(user_in)

    non_existent_todo_id = 999
    todo_update = TodoUpdate(
        title="Updated Todo", description="Updated description", done=True
    )

    with pytest.raises(HTTPException) as exc_info:
        todo_service.update_todo(non_existent_todo_id, todo_update, user.id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Todo not found"


def test_delete_todo_not_found(db_session):
    """
    Test deleting a non-existent todo item.

    Args:
        db_session: The database session fixture.

    Asserts:
        - An HTTPException is raised with the expected status code and detail message.
    """
    user_service = UserService(db_session)
    todo_service = TodoService(db_session)

    user_in = UserCreate(name=USER_NAME, email=unique_email())
    user = user_service.create_user(user_in)

    non_existent_todo_id = 999

    with pytest.raises(HTTPException) as exc_info:
        todo_service.delete_todo(non_existent_todo_id, user.id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Todo not found"
