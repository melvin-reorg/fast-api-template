"""Common utility functions"""

import uuid


def unique_email():
    return f"{uuid.uuid4()}@example.com"
