import pytest
from datetime import timedelta
from flask_jwt_extended import create_access_token
from app import create_app, db


@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-only-secret-key-with-32-plus-bytes'
    })

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def register_user(client, email="owner@example.com", password="password123"):
    return client.post("/api/signup", json={
        "name": "Test User",
        "email": email,
        "password": password,
    })


def login_headers(client, email="owner@example.com", password="password123"):
    response = client.post("/api/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.get_json()['access_token']}"}


def create_task(client, headers, **task_data):
    response = client.post("/api/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    return response.get_json()


def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code ==200
    assert response.get_json()=={"status":"ok"}


def test_app_rejects_short_jwt_secret():
    with pytest.raises(RuntimeError, match="at least 32 bytes"):
        create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "JWT_SECRET_KEY": "short",
        })

def test_signup(client):
    response =client.post('/api/signup', json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "test1234"
    })
    assert response.status_code==201
    assert response.get_json()["email"]=="test@example.com"


def test_signup_normalizes_email_and_rejects_duplicates(client):
    assert register_user(client).status_code == 201
    duplicate = register_user(client, " OWNER@EXAMPLE.COM ")
    assert duplicate.status_code == 409


def test_signup_stores_a_password_hash(client):
    assert register_user(client).status_code == 201
    from app.models.user import User

    with client.application.app_context():
        user = User.query.filter_by(email="owner@example.com").one()
        assert user.password_hash != "password123"
        assert user.check_password("password123")


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "Test", "email": "not-an-email", "password": "password123"},
        {"name": "Test", "email": "test@example.com", "password": "short"},
        {"name": "x" * 21, "email": "test@example.com", "password": "password123"},
    ],
)
def test_signup_rejects_invalid_auth_fields(client, payload):
    assert client.post("/api/signup", json=payload).status_code == 400
def test_singup_missing_fields(client):
    response =client.post('/api/signup', json={"email": "test@example.com"})
    assert response.status_code==400
def test_login_wrong_password(client):
    client.post('/api/signup', json={
        "name": "Test User",
        "email": "test2@example.com",
        "password": "correctpass"
    })
    response = client.post('/api/login', json={
        "email": "test2@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_task_routes_require_valid_jwt(client):
    register_user(client)
    assert client.get("/api/tasks").status_code == 401
    response = client.get("/api/tasks", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401


def test_task_routes_reject_expired_jwt(client):
    register_user(client)
    with client.application.app_context():
        expired_token = create_access_token("1", expires_delta=timedelta(seconds=-1))

    response = client.get(
        "/api/tasks", headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401


def test_owner_can_create_get_update_and_delete_task(client):
    register_user(client)
    headers = login_headers(client)
    task = create_task(client, headers, title="Write tests", description="Cover the API")

    fetched = client.get(f"/api/tasks/{task['id']}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.get_json()["title"] == "Write tests"

    updated = client.put(
        f"/api/tasks/{task['id']}",
        json={"status": "completed", "title": "Write thorough tests"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.get_json()["status"] == "completed"
    assert updated.get_json()["title"] == "Write thorough tests"

    deleted = client.delete(f"/api/tasks/{task['id']}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/api/tasks/{task['id']}", headers=headers).status_code == 404


def test_users_cannot_access_or_modify_other_users_tasks(client):
    register_user(client, "owner@example.com")
    owner_headers = login_headers(client, "owner@example.com")
    task = create_task(client, owner_headers, title="Private task")

    register_user(client, "other@example.com")
    other_headers = login_headers(client, "other@example.com")

    assert client.get(f"/api/tasks/{task['id']}", headers=other_headers).status_code == 404
    assert client.put(
        f"/api/tasks/{task['id']}", json={"title": "stolen"}, headers=other_headers
    ).status_code == 404
    assert client.delete(f"/api/tasks/{task['id']}", headers=other_headers).status_code == 404
    assert client.get("/api/tasks", headers=other_headers).get_json()["total"] == 0
    assert client.get(f"/api/tasks/{task['id']}", headers=owner_headers).status_code == 200


def test_task_filters_and_pagination(client):
    register_user(client)
    headers = login_headers(client)
    create_task(client, headers, title="First", priority="low")
    create_task(client, headers, title="Second", priority="high", status="completed")
    create_task(client, headers, title="Third", priority="high")

    filtered = client.get(
        "/api/tasks?priority=high&status=pending&page=1&per_page=1", headers=headers
    )
    payload = filtered.get_json()
    assert filtered.status_code == 200
    assert payload["total"] == 1
    assert payload["pages"] == 1
    assert payload["tasks"][0]["title"] == "Third"

    paged = client.get("/api/tasks?page=2&per_page=1", headers=headers).get_json()
    assert paged["total"] == 3
    assert paged["page"] == 2
    assert len(paged["tasks"]) == 1


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": "   "},
        {"title": "x" * 201},
        {"title": "Valid", "priority": "urgent"},
        {"title": "Valid", "status": "blocked"},
        {"title": "Valid", "description": 12},
        {"title": "Valid", "user_id": 999},
    ],
)
def test_invalid_task_payloads_are_rejected(client, payload):
    register_user(client)
    response = client.post("/api/tasks", json=payload, headers=login_headers(client))
    assert response.status_code == 400


@pytest.mark.parametrize(
    "query",
    ["?page=0", "?page=abc", "?per_page=0", "?per_page=101", "?status=blocked", "?priority=urgent"],
)
def test_invalid_task_query_parameters_are_rejected(client, query):
    register_user(client)
    response = client.get(f"/api/tasks{query}", headers=login_headers(client))
    assert response.status_code == 400


def test_invalid_update_does_not_change_task(client):
    register_user(client)
    headers = login_headers(client)
    task = create_task(client, headers, title="Keep this title")

    response = client.put(
        f"/api/tasks/{task['id']}", json={"status": "invalid"}, headers=headers
    )
    assert response.status_code == 400
    assert client.get(f"/api/tasks/{task['id']}", headers=headers).get_json()["title"] == "Keep this title"
