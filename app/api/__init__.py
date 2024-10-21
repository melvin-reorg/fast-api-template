from fastapi import APIRouter
from .health import api as healthcheck
from .users import api as users
from .todos import api as todos

# Create an instance of APIRouter
router = APIRouter()

# Include the healthcheck router with the tag "Health"
router.include_router(healthcheck.router, tags=["Health"])

# Include the users router with the tag "Users"
router.include_router(users.router, tags=["Users"])

# Include the todos router with the tag "Todos"
router.include_router(todos.router, tags=["Todos"])
