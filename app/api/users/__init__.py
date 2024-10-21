"""
This module initializes the `users` package by importing the `User` model
from the `models` submodule and making it available for import when the
`users` package is imported.

Attributes:
    __all__ (list): A list of public objects of this module, as interpreted
                    by `import *`. It contains the string "User".
"""

from .models import User

__all__ = ["User"]