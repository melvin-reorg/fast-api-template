"""
This module contains the SQLAlchemy model for the Todo resource.
"""

from app.database.config import DBBase
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship

from datetime import datetime, timezone


class Todo(DBBase):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    done = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="todos")

    __table_args__ = (Index("ix_todo_title", "title"),)

    def __repr__(self):
        return f"<Todo id={self.id} title={self.title} done={self.done}>"
