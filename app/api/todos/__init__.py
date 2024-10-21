"""
This module initializes the `todos` package by importing the `Todo` model
and defining the `__all__` list to specify the public interface of the module.

Attributes:
    __all__ (list): A list containing the names of the objects that should be
    accessible when the module is imported using `from module import *`.
"""

from .models import Todo

__all__ = ["Todo"]