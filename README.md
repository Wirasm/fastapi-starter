# FastAPI Starter Template

This is a modular monolithic starter template for FastAPI, designed to provide a robust foundation for your projects with async capabilities and flexible deployment options.

## Features

- Fully async FastAPI setup
- PostgreSQL database with SQLAlchemy (async)
- JWT authentication
- Modular structure for easy expansion
- Docker support with hot-reload
- Environment variable configuration
- Logging and centralized error handling
- Unit and integration tests with pytest
- Ruff for linting and formatting
- Alembic migrations with async support

## Prerequisites

- Python 3.12+
- Poetry
- Docker and Docker Compose (for containerized setup)

## Quick Start with Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/fastapi-starter.git
   cd fastapi-starter
   ```

2. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

3. Start the services:

   ```bash
   docker compose up --build
   ```

4. Visit `http://localhost:8000/docs` to see the API documentation.

## Local Development Setup

1. Install dependencies:

   ```bash
   poetry install
   ```

2. Set up your environment variables:

   ```bash
   cp .env.example .env
   ```

3. Start PostgreSQL:

   ```bash
   docker compose up -d db
   ```

4. Run migrations:

   ```bash
   poetry run alembic upgrade head
   ```

5. Start the application:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

## Database Management

### Running Migrations

With Docker:

```bash
docker compose exec web alembic upgrade head
```

Locally:

```bash
poetry run alembic upgrade head
```

### Creating New Migrations

```bash
poetry run alembic revision --autogenerate -m "Description of changes"
```

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

```bash
poetry run pytest
```

For test coverage:

```bash
poetry run pytest --cov=src
```

## Code Quality

Linting:

```bash
poetry run ruff check .
```

Formatting:

```bash
poetry run ruff format .
```

## Project Structure

```
fastapi-starter/
├── src/                    # Application source code
│   ├── auth/              # Authentication module
│   │   ├── models.py      # User model
│   │   ├── router.py      # Auth routes
│   │   └── jwt.py         # JWT handling
│   ├── items/             # Items module
│   │   ├── models.py      # Item model
│   │   ├── router.py      # Item routes
│   │   └── schemas.py     # Pydantic schemas
│   ├── core/              # Core functionality
│   │   ├── config.py      # Configuration
│   │   ├── exceptions.py  # Exception handling
│   │   └── logging.py     # Logging setup
│   ├── database/          # Database setup
│   │   ├── database.py    # Database configuration
│   │   └── models.py      # Base models
│   └── main.py            # Application entry point
├── tests/                 # Test suite
├── alembic/               # Database migrations
├── claudeDev_docs/        # Development documentation
├── docker-compose.yml     # Docker services configuration
├── Dockerfile            # Application container definition
├── pyproject.toml        # Project dependencies and config
└── README.md             # Project documentation
```

## Environment Variables

Key environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `HOST`: Application host (default: 0.0.0.0)
- `PORT`: Application port (default: 8000)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
