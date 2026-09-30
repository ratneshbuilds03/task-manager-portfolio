# Task Manager - Full Stack Task Management System

A full-stack task management application built for a backend developer portfolio. It pairs a Flask REST API with a React/Vite client, MySQL persistence, JWT authentication, automated tests, and local Docker Compose support. There is no deployed instance or live demo.

## Features

- User signup and login with bcrypt password hashing and JWT access tokens
- User-owned task CRUD with ownership enforced on every task endpoint
- Task status and priority validation, filtering, and bounded pagination
- React screens for authentication, task creation/editing, completion, filtering, and pagination
- MySQL-backed API and a SQLite in-memory database for isolated pytest runs
- Docker Compose for local API and MySQL development
- GitHub Actions checks for backend tests, frontend build, and Docker image build

## Technology

- Backend: Python 3.14, Flask, Flask-SQLAlchemy, SQLAlchemy, PyMySQL
- Authentication: Flask-JWT-Extended and bcrypt
- Frontend: React 18, React Router 7, Vite 8, Axios
- Database: MySQL 8
- Quality: pytest, npm audit, GitHub Actions

## Architecture

The browser sends JSON requests through Axios to the Flask API. Flask routes validate requests and JWTs, service functions apply task ownership and business rules, and SQLAlchemy persists records in MySQL. Signup returns a user object; login returns an access token and user data. The frontend sends the token as a Bearer token on protected task requests.

## Local Setup

### Backend and MySQL

1. Install Python 3.14 and MySQL 8, or use Docker Compose for MySQL.
2. Copy `.env.example` to `.env` and replace the example passwords and JWT key with local values. Generate a key with `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
3. For a local MySQL server, set `MYSQL_HOST=localhost`, create the database and configured MySQL user, and leave `DATABASE_URL` blank to use the component settings. For Compose, keep `MYSQL_HOST=localhost` in `.env`; Compose overrides it to the `db` service for the API container.
4. Create a virtual environment and install dependencies:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

5. Start the API with `python run.py`. It listens on `http://localhost:5000`; tables are created at startup.

### Frontend

In another terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Vite serves the frontend at `http://localhost:3000` and proxies `/api` requests to the local API. `VITE_API_URL` can override that base URL; `.env.example` uses the proxy path.

### Docker Compose

After creating and editing the root `.env` file:

```powershell
docker compose up --build
```

Compose starts the API on port 5000 and MySQL on port 3307. Start the frontend separately using the steps above. Stop the containers with `docker compose down`; the named MySQL volume is retained.

## Environment Variables

| Variable              | Purpose                                                                 |
| --------------------- | ----------------------------------------------------------------------- |
| `MYSQL_ROOT_PASSWORD` | Local MySQL root password required by the container                     |
| `MYSQL_USER`          | Application MySQL user                                                  |
| `MYSQL_PASSWORD`      | Application MySQL password                                              |
| `MYSQL_DATABASE`      | Database name                                                           |
| `MYSQL_HOST`          | MySQL host (`localhost` locally; Compose sets `db` for the API)         |
| `DATABASE_URL`        | Optional full SQLAlchemy MySQL URL; overrides the component settings    |
| `JWT_SECRET_KEY`      | Secret used to sign JWTs; provide a random value of at least 32 bytes   |
| `CORS_ORIGINS`        | Comma-separated allowed browser origins; defaults to local Vite origins |
| `FLASK_DEBUG`         | Enables Flask debug mode only when explicitly set to `true`             |
| `VITE_API_URL`        | Optional frontend API base URL; defaults to `/api`                      |

`.env` is ignored by Git and Docker. Only the safe `.env.example` template belongs in the repository. If `DATABASE_URL` contains special characters in its password, URL-encode them; the component-based MySQL settings are encoded by the application.

## API Overview

All endpoints are under `/api`.

| Method   | Path              | Authentication | Result                                        |
| -------- | ----------------- | -------------- | --------------------------------------------- |
| `GET`    | `/api/health`     | No             | API health response                           |
| `POST`   | `/api/signup`     | No             | Creates a user; duplicate email returns `409` |
| `POST`   | `/api/login`      | No             | Returns `access_token` and user data          |
| `GET`    | `/api/tasks`      | Bearer token   | Lists only the caller's tasks                 |
| `POST`   | `/api/tasks`      | Bearer token   | Creates a task for the caller                 |
| `GET`    | `/api/tasks/<id>` | Bearer token   | Gets an owned task; otherwise `404`           |
| `PUT`    | `/api/tasks/<id>` | Bearer token   | Updates an owned task; otherwise `404`        |
| `DELETE` | `/api/tasks/<id>` | Bearer token   | Deletes an owned task and returns `204`       |

The task list accepts `status`, `priority`, `page`, and `per_page`. Status values are `pending`, `in_progress`, and `completed`; priority values are `low`, `medium`, and `high`. `per_page` must be between 1 and 100. The list response includes `tasks`, `total`, `page`, `per_page`, and `pages`. Create and update requests accept `title`, `description`, `status`, and `priority`; unsupported or invalid values return `400`.

## Tests and CI

Run the backend tests with:

```powershell
python -m pytest -q
```

The suite uses an in-memory SQLite database and covers signup/login, password hashing, JWT failures, task CRUD, ownership isolation, validation, filtering, and pagination. MySQL is not required for pytest.

GitHub Actions runs the backend tests, builds the Docker image, installs the locked frontend dependencies with `npm ci`, and builds the frontend. It does not deploy or publish the application.

## Project Structure

```text
app/                 Flask application, models, routes, services, and errors
frontend/            React/Vite application and API client
tests/                pytest API behavior tests
.github/workflows/    GitHub Actions CI
Dockerfile            Backend image definition
docker-compose.yml    Local API and MySQL services
.env.example          Safe local environment template
requirements.txt      Python dependencies
```

## Future Improvements

- Add database migrations before changing deployed schemas
- Add refresh-token/session revocation support
- Add rate limiting and stronger signup email verification
- Add frontend component and browser integration tests

## License

No license file is included. Add a license before granting reuse or redistribution rights.
