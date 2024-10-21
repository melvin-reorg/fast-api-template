#!/bin/bash

# run migrations
alembic upgrade head

# Start the server
python main.py