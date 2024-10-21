import pytest

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from app.api.todos.schemas import TodoCreate
from app.api.todos.services import TodoService
from app.api.users.models import User as UserModel
from app.api.users.schemas import UserCreate, UserUpdate
from app.api.users.services import UserService
from app.utils.common import unique_email


USER = "Pancho Mancho"


def test_create_user(db_session):
    """
    Test the creation of a user.

    Args:
        db_session: The database session.

    Asserts:
        - The user ID is not None.
        - The user name matches the expected name.
        - The user email matches the expected email.
    """
    user_service = UserService(db_session)
    email = unique_email()
    user_in = UserCreate(name=USER, email=email)
    user = user_service.create_user(user_in)

    assert user.id is not None
    assert user.name == USER
    assert user.email == email


def test_get_user(db_session):
    """
    Test retrieving a user by ID.

    Args:
        db_session: The database session.

    Asserts:
        - The retrieved user ID matches the expected ID.
        - The retrieved user name matches the expected name.
        - The retrieved user email matches the expected email.
        - The retrieved user has no todos.
    """
    user_service = UserService(db_session)
    email = unique_email()
    user_in = UserCreate(name=USER, email=email)
    user = user_service.create_user(user_in)

    retrieved_user = user_service.get_user(user.id)

    assert retrieved_user.id == user.id
    assert retrieved_user.name == USER
    assert retrieved_user.email == email
    assert retrieved_user.todos == []


def test_create_todo_for_user(db_session):
    """
    Test creating a todo for a user.

    Args:
        db_session: The database session.

    Asserts:
        - The todo ID is not None.
        - The todo title matches the expected title.
        - The todo description matches the expected description.
        - The todo is not marked as done.
        - The todo user ID matches the expected user ID.
    """
    user_service = UserService(db_session)
    todo_service = TodoService(db_session)

    email = unique_email()

    user_in = UserCreate(name=USER, email=email)
    user = user_service.create_user(user_in)

    todo_in = TodoCreate(
        title="Test Todo", description="This is a test todo", done=False
    )
    todo = todo_service.create_todo(todo_in, user.id)

    assert todo.id is not None
    assert todo.title == "Test Todo"
    assert todo.description == "This is a test todo"
    assert todo.done is False
    assert todo.user_id == user.id


def test_get_user_with_todos(db_session):
    """
    Test retrieving a user with todos.

    Args:
        db_session: The database session.

    Asserts:
        - The retrieved user ID matches the expected ID.
        - The retrieved user has the expected number of todos.
        - The titles of the retrieved todos match the expected titles.
    """
    user_service = UserService(db_session)
    todo_service = TodoService(db_session)

    email = unique_email()

    user_in = UserCreate(name=USER, email=email)
    user = user_service.create_user(user_in)

    todo_in = TodoCreate(title="Todo 1", description="First todo", done=False)
    todo_service.create_todo(todo_in, user.id)

    todo_in = TodoCreate(title="Todo 2", description="Second todo", done=False)
    todo_service.create_todo(todo_in, user.id)

    retrieved_user = user_service.get_user(user.id)

    assert retrieved_user.id == user.id
    assert len(retrieved_user.todos) == 2
    assert retrieved_user.todos[0].title == "Todo 1"
    assert retrieved_user.todos[1].title == "Todo 2"


def test_create_user_failure(db_session, mocker):
    """
    Test user creation failure due to a simulated database error.

    Args:
        db_session: The database session.
        mocker: The mocker object to patch methods.

    Asserts:
        - An HTTPException is raised with status code 400.
        - The exception detail contains the expected error message.
    """
    user_service = UserService(db_session)
    email = unique_email()
    user_in = UserCreate(name=USER, email=email)

    # Simulate an exception when adding a user
    mocker.patch.object(
        db_session, "add", side_effect=SQLAlchemyError("Simulated database error")
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(user_in)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Error creating user" in exc_info.value.detail


def test_get_user_not_found(db_session):
    """
    Test retrieving a user that does not exist.

    Args:
        db_session: The database session.

    Asserts:
        - An HTTPException is raised with status code 404.
        - The exception detail contains the expected error message.
    """
    user_service = UserService(db_session)
    user_id = 999

    # Simulate user not found
    db_session.query(UserModel).filter().first = None

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        user_service.get_user(user_id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "User not found"


def test_update_user_not_found(db_session):
    """
    Test updating a user that does not exist.

    Args:
        db_session: The database session.

    Asserts:
        - An HTTPException is raised with status code 404.
        - The exception detail contains the expected error message.
    """
    user_service = UserService(db_session)
    user_id = 999
    email = unique_email()
    user_in = UserUpdate(name=USER, email=email)

    # Simulate user not found
    db_session.query(UserModel).filter().first = None

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        user_service.update_user(user_id, user_in)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "User not found"


def test_delete_user_not_found(db_session):
    """
    Test deleting a user that does not exist.

    Args:
        db_session: The database session.

    Asserts:
        - An HTTPException is raised with status code 404.
        - The exception detail contains the expected error message.
    """
    user_service = UserService(db_session)
    user_id = 999

    # Simulate user not found
    db_session.query(UserModel).filter().first = None

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        user_service.delete_user(user_id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "User not found"
