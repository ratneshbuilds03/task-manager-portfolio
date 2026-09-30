# 📝 Task Manager

> A full-stack task management application built with **Flask, React, MySQL, JWT Authentication, Docker, and GitHub Actions**.

Task Manager is a full-stack web application that provides secure user authentication and task management through a RESTful API and a React-based frontend.

The project focuses on clean backend architecture, JWT-based authentication, user-specific task ownership, database integration, automated testing, containerization, and CI validation.

---

## ✨ Features

### 🔐 Authentication & Security

* User registration and login
* JWT-based authentication
* Password hashing with bcrypt
* Protected API endpoints
* User-specific task ownership
* Users can access only their own tasks
* Environment-based configuration for sensitive values

### 📋 Task Management

* Create tasks
* View tasks
* Update tasks
* Delete tasks
* Task ownership validation
* Protected task operations

### 🖥️ Frontend

* React + Vite
* Authentication flow
* Task management interface
* API integration with Flask backend
* API base URL configured through `/api`

### 🧪 Testing

* Pytest-based backend test suite
* Authentication tests
* Task CRUD tests
* Authorization and ownership tests
* Error-handling tests

**Current test status:**

```text
29 passed
```

### 🐳 Docker

* Backend containerization
* Docker Compose configuration
* Environment-based Docker configuration
* Easy local development setup

### ⚙️ CI/CD

GitHub Actions is configured to automatically validate the project during development.

The CI workflow runs the project's automated checks and helps prevent broken changes from being merged.

---

## 🛠️ Tech Stack

| Layer            | Technology     |
| ---------------- | -------------- |
| Backend          | Flask          |
| API              | REST API       |
| Frontend         | React + Vite   |
| Database         | MySQL          |
| Authentication   | JWT            |
| Password Hashing | bcrypt         |
| Testing          | Pytest         |
| Containerization | Docker         |
| Orchestration    | Docker Compose |
| CI               | GitHub Actions |
| Version Control  | Git & GitHub   |

---

## 🏗️ Project Architecture

```text
task-manager/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── models/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── docker-compose.yml
├── .github/
│   └── workflows/
│
├── .env.example
└── README.md
```

> The structure above represents the major project components. Refer to the repository for the complete implementation structure.

---

## 🔑 Authentication Flow

The application uses JWT-based authentication.

```text
User
 │
 ├── Signup
 │      ↓
 │   Password Hashing
 │      ↓
 │   MySQL
 │
 └── Login
        ↓
     JWT Token
        ↓
   Protected API
        ↓
   Task Operations
```

Protected endpoints require a valid authentication token.

Task ownership is also checked so that authenticated users can operate only on their own tasks.

---

## 🌐 API Overview

The backend API uses the `/api` prefix.

### Authentication

| Method | Endpoint      | Description                      |
| ------ | ------------- | -------------------------------- |
| POST   | `/api/signup` | Register a new user              |
| POST   | `/api/login`  | Authenticate user and obtain JWT |

### Tasks

| Method    | Endpoint          | Description                    |
| --------- | ----------------- | ------------------------------ |
| GET       | `/api/tasks`      | Get authenticated user's tasks |
| POST      | `/api/tasks`      | Create a task                  |
| PUT/PATCH | `/api/tasks/<id>` | Update a task                  |
| DELETE    | `/api/tasks/<id>` | Delete a task                  |

> Exact request and response formats are documented by the implementation and can be explored through the API source/tests.

---

## 🗄️ Database

The application uses **MySQL** for persistent data storage.

The database stores application data including:

* Users
* Tasks
* User-task ownership relationships

Sensitive database credentials are **not stored directly in the source code**.

Environment variables are used for configuration.

---

## ⚙️ Environment Variables

Create environment files from the provided examples.

Example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure the required values in `.env`.

### 🔒 Security

Never commit real credentials or secrets to GitHub.

Sensitive values such as:

* Database passwords
* JWT secrets
* API credentials

should remain in environment variables.

The repository contains example configuration files with placeholder values.

---

## 🚀 Local Development

### 1. Clone the repository

```bash
git clone https://github.com/ratneshbuilds03/task-manager-portfolio.git
cd task-manager-portfolio
```

### 2. Backend setup

Create and activate a virtual environment:

```powershell
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Configure your environment variables using `.env.example`.

Start the Flask backend using the project's configured application entry point.

---

## 🎨 Frontend Setup

The frontend runs separately from the backend Docker container.

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The React frontend communicates with the Flask API through the configured `/api` base path.

---

## 🐳 Running with Docker

Build and start the services:

```bash
docker compose up --build
```

To stop the services:

```bash
docker compose down
```

Environment configuration should be provided through the appropriate environment file described in the repository.

---

## 🧪 Running Tests

From the backend project directory:

```bash
pytest
```

Current verified result:

```text
29 passed
```

The test suite covers areas including:

* Authentication
* User registration/login
* Task CRUD operations
* Authorization
* Task ownership
* Error handling

---

## 🔄 Continuous Integration

The project includes a **GitHub Actions** workflow for automated validation.

The CI pipeline helps verify that changes continue to pass the project's automated checks.

Workflow files are available under:

```text
.github/workflows/
```

---

## 📂 Project Highlights

This project demonstrates practical experience with:

* REST API development
* Flask backend architecture
* JWT authentication
* Secure password hashing
* MySQL database integration
* Authorization and resource ownership
* React frontend integration
* Automated testing with Pytest
* Docker containerization
* Docker Compose
* GitHub Actions CI
* Environment-based secret management

---

## 🔮 Future Improvements

Possible future improvements include:

* Task filtering and advanced search
* Task priorities and categories
* Due-date and reminder support
* Pagination for larger task lists
* Improved frontend UI/UX
* Additional automated test coverage

These are potential future enhancements and are **not currently presented as implemented features**.

---

## 📌 Project Status

**Status:** Completed portfolio project

The project is maintained as a demonstration of full-stack development, backend API design, authentication, database integration, testing, Docker, and CI practices.

---

## 👨‍💻 Author

**Ratnesh Makwana**

Backend Engineer | Python | Flask | FastAPI | REST APIs | MySQL | Docker

---

⭐ If you find this project useful, feel free to explore the repository and review the implementation.
