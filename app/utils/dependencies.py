"""This module contains common dependencies used in the application"""

from app.database.config import SessionLocal


def get_db():
    """This function starts a db session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
