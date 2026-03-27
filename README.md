# Evently API

A Flask-based REST API for managing events and RSVPs with different access levels. This API is designed to teach web security best practices through incremental improvements.

## Project Context

This repo was created as an assignment during my training as a QA Engineer. The **Flask API itself was provided as starter code** -- my task was to build a complete testing and CI/CD pipeline around it.

### Provided (Starter Code)
- Flask application with authentication, event, and RSVP endpoints (`app.py`, `models.py`, `config.py`, `routes/`)
- OpenAPI specification (`openapi.yaml`)
- Dependencies (`requirements.txt`)

### My Contribution
- **Test suite** -- API integration tests and unit tests with pytest (`tests/`)
  - Client pattern (similar to Page Object Model) for better maintainability (`tests/api_clients/`)
  - Fixtures and test data generation (`tests/conftest.py`)
- **CI/CD pipeline** -- GitHub Actions workflow that automatically builds and tests on every push (`.github/workflows/ci_workflow.yml`)
- **Dockerization** -- Dockerfile and .dockerignore for containerized execution
- **README extension** -- Documentation of Docker setup, CI/CD, test architecture, and Swagger UI

## Features

- **Public Events**: Anyone can RSVP without authentication
- **Protected Events**: Requires user authentication to RSVP
- **Admin Events**: Requires admin role to RSVP

## Tech Stack

- Flask 3.0.0
- Flask-SQLAlchemy (SQLite database)
- Flask-CORS
- Flask-JWT-Extended (JWT authentication)

## Setup

1. Create and activate a virtual environment:

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux/Mac:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

# Docker

The application can be run in a Docker container.

1. Build the Docker image:
```bash
docker build -t events-api .
```

2. Run the container:
```bash
docker run -d -p 5000:5000 --name events_api_container events-api
```

3. Verify the API is running:
```bash
curl localhost:5000/api/health
```

4. Stop and remove the container:
```bash
docker stop events_api_container
docker rm events_api_container
```

## CI/CD

This project uses **GitHub Actions** for continuous integration. The pipeline is triggered on every push or pull request to `main` and performs the following steps:

1. Checks out the repository
2. Builds the Docker image
3. Starts the container and runs a health check
4. Sets up Python and installs dependencies
5. Runs the full test suite against the containerized API
6. Cleans up the container

The workflow configuration can be found in `.github/workflows/ci_workflow.yml`.

## Swagger UI Documentation

The API includes interactive Swagger UI documentation. After starting the server:

1. Open your browser and navigate to: `http://localhost:5000/apidocs`

2. You'll see an interactive API documentation interface where you can:
   - Browse all available endpoints
   - See request/response schemas
   - Test endpoints directly from the browser
   - Authenticate using the "Authorize" button (enter your JWT token)

3. To use the "Authorize" button:
   - First, login via `/api/auth/login` to get your JWT token
   - Click the "Authorize" button at the top of the Swagger UI
   - Enter: `Bearer <your_jwt_token>` (replace `<your_jwt_token>` with your actual token)
   - Now you can test protected endpoints directly from Swagger UI

**Alternative**: You can also view the OpenAPI specification directly at `http://localhost:5000/apispec_1.json`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
  ```json
  {
    "username": "user123",
    "password": "password123"
  }
  ```

- `POST /api/auth/login` - Login and get JWT token
  ```json
  {
    "username": "user123",
    "password": "password123"
  }
  ```

### Events

- `GET /api/events` - Get all events
- `GET /api/events/<id>` - Get a specific event
- `POST /api/events` - Create a new event (requires authentication)
  ```json
  {
    "title": "Python Meetup",
    "description": "Monthly Python developer meetup",
    "date": "2026-01-15T18:00:00",
    "location": "Tech Hub, Room 101",
    "capacity": 50,
    "is_public": true,
    "requires_admin": false
  }
  ```

### RSVPs

- `POST /api/rsvps/event/<event_id>` - RSVP to an event
  ```json
  {
    "attending": true
  }
  ```

- `GET /api/rsvps/event/<event_id>` - Get all RSVPs for an event

## Authentication

For protected endpoints, include the JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

# Test Architecture

Tests are located in the `tests/` directory and use `pytest` with `requests` for HTTP-based API testing.

```
tests/
  api_clients/          # Client classes for API interaction
    auth_client.py      # AuthClient: register, login
    events_client.py    # EventsClient: create_event
    rsvps_client.py     # RSVPSClient: rsvp_to_event
  conftest.py           # Fixtures and shared test data
  test_api.py           # API integration tests
  test_models.py        # Unit tests for data models
```

The test suite follows a **client pattern** (similar to Page Object Model for UI tests): each API endpoint group has a dedicated client class that encapsulates HTTP calls. Tests use these clients instead of making raw `requests` calls, improving readability and maintainability.

### Running Tests

1. Install test dependencies:
```bash
pip install -r requirements-test.txt
```

2. Make sure the API is running (locally or in Docker), then:
```bash
pytest -v
```

## Security Notes

This is a basic implementation designed for educational purposes. The following security considerations are intentionally simplified and can be improved in subsequent lessons:

- Password storage (currently using werkzeug, but can be improved)
- JWT token handling
- Input validation
- SQL injection prevention (SQLAlchemy helps, but can be improved)
- Rate limiting
- CORS configuration
- Error handling and information disclosure

## Database

The application uses SQLite by default. The database file (`events.db`) will be created automatically on first run.

**Note**: The first user registered automatically becomes an admin for demo purposes.

