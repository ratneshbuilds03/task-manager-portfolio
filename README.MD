# Task Manager - Full-Stack Task Management System

A portfolio project demonstrating a Flask REST API and React client for personal task tracking. It uses MySQL for application data, JWT bearer tokens for authentication, bcrypt for password hashing, pytest for backend tests, and Docker Compose for local API and database development. **This project is not deployed and has no live demo.**

## Features

- User signup and login; passwords are stored as bcrypt hashes.
- JWT-protected task endpoints with user-specific task ownership.
- Create, read, update, and delete tasks.
- Validate task titles, descriptions, status, priority, filters, and pagination.
- Filter tasks by status and priority; paginate list responses.
- React screens for authentication, task editing, completion toggling, filtering, and pagination.
- Isolated backend tests using an in-memory SQLite database.
- GitHub Actions checks for backend tests, frontend dependency audit/build, and Docker image build.

## Technology

| Area                      | Technologies                                              |
| ------------------------- | --------------------------------------------------------- |
| Backend                   | Python 3.14, Flask, Flask-SQLAlchemy, SQLAlchemy, PyMySQL |
| Authentication            | Flask-JWT-Extended, bcrypt                                |
| Frontend                  | React 18, React Router 7, Vite 8, Axios, React Icons      |
| Database                  | MySQL 8; SQLite in-memory for pytest                      |
| Quality and local tooling | pytest, npm, Docker, Docker Compose, GitHub Actions       |

## Architecture

```text
React browser client
  -> Axios JSON requests (Vite proxies /api during local development)
  -> Flask blueprints (/api)
  -> request validation and JWT checks
  -> service functions enforce task ownership
  -> SQLAlchemy models and MySQL
```

The app factory in `app/__init__.py` initializes Flask, SQLAlchemy, JWT, CORS, error handlers, and the API blueprints. The task service scopes task reads and mutations to the authenticated user's ID. Tables are created with SQLAlchemy `db.create_all()` at application startup; a migration tool is not included.

### Project structure

```text
app/
  models/          User and Task SQLAlchemy models
  routes/          Authentication and task API blueprints
  services/        Authentication and task business logic
  utils/           API error handlers
tests/             pytest API behavior tests
frontend/
  src/pages/       Login, signup, and dashboard
  src/components/  Task form, list, and card
  src/services/    Axios API client
.github/workflows/ GitHub Actions CI
Dockerfile         Backend image
docker-compose.yml Local API and MySQL services
.env.example       Safe root environment template
```

## Authentication and Authorization

- `POST /api/signup` validates the name, email, and password; passwords are hashed with bcrypt. A duplicate email returns `409`.
- `POST /api/login` verifies credentials and returns `access_token` plus user data.
- The frontend sends the token in the `Authorization: Bearer <token>` header for task requests.
- Missing, invalid, or expired tokens receive `401` responses.
- Every task endpoint requires authentication. Task queries include the token's user ID; another user's task is treated as not found (`404`).
- The browser client stores the access token and user data in `localStorage` and clears them when an API response indicates an unauthorized session.

## Task Management

Tasks have a title, optional description, status, priority, creation timestamp, and owning user ID. Supported statuses are `pending`, `in_progress`, and `completed`; priorities are `low`, `medium`, and `high`.

The task list accepts `status`, `priority`, `page`, and `per_page`. Defaults are page `1` and 10 results per page; `per_page` is limited to 1-100. Its response includes `tasks`, `total`, `page`, `per_page`, and `pages`. `PUT` accepts one or more supported task fields. Invalid or unsupported values return `400`.

## API Overview

All routes are registered under `/api`.

| Method   | Route                  | Auth         | Behavior                                                  |
| -------- | ---------------------- | ------------ | --------------------------------------------------------- |
| `GET`    | `/api/health`          | No           | Returns API health status                                 |
| `POST`   | `/api/signup`          | No           | Creates an account; duplicate email returns `409`         |
| `POST`   | `/api/login`           | No           | Verifies credentials and returns an access token          |
| `GET`    | `/api/tasks`           | Bearer token | Lists the caller's tasks; supports filters and pagination |
| `POST`   | `/api/tasks`           | Bearer token | Creates a task for the caller                             |
| `GET`    | `/api/tasks/<task_id>` | Bearer token | Gets an owned task; otherwise returns `404`               |
| `PUT`    | `/api/tasks/<task_id>` | Bearer token | Updates supplied fields on an owned task                  |
| `DELETE` | `/api/tasks/<task_id>` | Bearer token | Deletes an owned task; returns `204`                      |

## Database

MySQL is the application database. `User` records have a unique email and password hash. `Task.user_id` is a non-null foreign key to `users.id`, supporting per-user task ownership. SQLAlchemy creates the tables during app startup; schema migrations are not configured. Pytest overrides the database URL with in-memory SQLite, so running the backend tests does not require MySQL.

## Frontend

The React single-page app provides `/login`, `/signup`, and `/dashboard` views. Axios uses `/api` by default, and the Vite development server proxies that path to `http://127.0.0.1:5000`. Set `VITE_API_URL` only when the API is hosted at another base URL. The frontend is started separately; it is not included in the Docker image or Compose services.

## Local Development

### Prerequisites

- Python 3.14
- Node.js 24 and npm
- MySQL 8 for running the backend directly, or Docker with the Compose plugin for the containerized API/database setup

### Configure environment

From the repository root, create a local env file from the safe template and edit its placeholder values:

```powershell
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(48))"
notepad .env
```

Use the generated random value for `JWT_SECRET_KEY`. Set the MySQL root and application-user passwords before starting Compose. `.env` is ignored by Git and excluded from the Docker build context; do not commit it. `frontend/.env.example` documents the optional frontend setting. Vite defaults to `/api`, so no frontend env file is needed for the local proxy.

### Run API and frontend locally

Start MySQL separately, create the configured database and application user, then configure `.env` for that server (`MYSQL_HOST=localhost`, database name, user, and password). From the repository root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

The API listens on `http://localhost:5000` by default. In another terminal:

```powershell
npm --prefix frontend ci
npm --prefix frontend run dev
```

Vite serves the client at `http://localhost:3000`.

### Run with Docker Compose

After creating and editing the root `.env` file as described above:

```powershell
docker compose up --build
```

Compose starts the Flask API on port `5000` and MySQL on host port `3307`. The API connects to the database service by the Compose hostname `db`. Start the frontend separately with the npm commands above. Stop the local services with `docker compose down`; the named MySQL volume is retained.

### Environment variables

| Variable              | Purpose                                                                 |
| --------------------- | ----------------------------------------------------------------------- |
| `MYSQL_ROOT_PASSWORD` | MySQL container root password                                           |
| `MYSQL_USER`          | Application MySQL user created by the MySQL image                       |
| `MYSQL_PASSWORD`      | Application user's MySQL password                                       |
| `MYSQL_DATABASE`      | Database name                                                           |
| `MYSQL_HOST`          | Database host; Compose overrides this to `db` for the API container     |
| `DATABASE_URL`        | Optional MySQL/PyMySQL SQLAlchemy URL; overrides component settings     |
| `JWT_SECRET_KEY`      | JWT signing secret; the app requires at least 32 bytes                  |
| `CORS_ORIGINS`        | Comma-separated allowed browser origins; defaults to local Vite origins |
| `FLASK_DEBUG`         | Enables Flask debug mode only when set to `true`                        |
| `PORT`                | API port; defaults to `5000`                                            |
| `VITE_API_URL`        | Optional frontend API base URL; defaults to `/api`                      |

When setting `DATABASE_URL` directly, use a MySQL URL and URL-encode special characters in credentials. The component-based MySQL settings encode the username, password, and database name when constructing the URL.

## Testing

Run the backend suite from the repository root:

```powershell
python -m pytest -q
```

**Latest verified result in this clean repository: `29 passed`.** The suite covers signup/login, password hashing, token rejection, task CRUD, user isolation, validation, filters, and pagination. It uses SQLite in memory and does not exercise a live MySQL server.

## Docker

`Dockerfile` builds the Flask API image only. It installs the Python requirements, copies the backend, and runs as a non-root user. `docker-compose.yml` adds MySQL for local development. No deployment or image-publishing workflow is configured.

## GitHub Actions

`.github/workflows/ci.yml` runs on pushes and pull requests targeting `main` or `master`. The backend job installs Python 3.14 dependencies, runs pytest, and builds the Docker image. The frontend job uses Node.js 24, runs `npm ci`, `npm audit --audit-level=moderate`, and `npm run build`. The workflow does not deploy or publish artifacts.

## Security Notes

- Keep database passwords and JWT signing keys in ignored local `.env` files or the runtime environment; never put real credentials in source or example templates.
- Commit only placeholder values in `.env.example` and `frontend/.env.example`.
- The API rejects missing, invalid, and expired JWTs and scopes task operations to their owner.
- Rotate any credential that has been exposed; deleting it from the current files does not remove it from Git history.

## Future Work

These are possible follow-ups, not current features:

- Add schema migrations before evolving the database model.
- Add refresh-token/session revocation and API rate limiting.
- Add frontend component or browser integration tests.
- Add optional email verification for account signup.
