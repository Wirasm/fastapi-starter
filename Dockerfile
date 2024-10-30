# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy project
COPY . /app

# Create a script to run migrations and start the application
RUN echo '#!/bin/sh\n\
    alembic upgrade head\n\
    uvicorn src.main:app --host 0.0.0.0 --port 8000\n\
    ' > /app/start.sh \
    && chmod +x /app/start.sh

# Run the script
CMD ["/app/start.sh"]
