from fastapi import Depends, APIRouter
from backend.app.main import app
from backend.app.api import deps
from backend.app.models.user import UserRole
from backend.app.crud.user import user_repository
from backend.app.schemas.user import UserCreate

# Register a temporary test route on app to test Role-Based Access Control (RBAC)
rbac_test_router = APIRouter(tags=["Test RBAC"])

@rbac_test_router.get("/api/v1/test-admin-only")
def endpoint_admin_only(
    admin_user = Depends(deps.RoleChecker([UserRole.ADMIN]))
):
    return {"status": "success", "role": admin_user.role}

@rbac_test_router.get("/api/v1/test-analyst-only")
def endpoint_analyst_only(
    analyst_user = Depends(deps.RoleChecker([UserRole.ANALYST, UserRole.ADMIN]))
):
    return {"status": "success", "role": analyst_user.role}

app.include_router(rbac_test_router)


def test_register_user_success(client):
    """Tests successful user registration"""
    payload = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "strongpassword123",
        "role": "business_user"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["full_name"] == "Test User"
    assert data["role"] == "business_user"
    assert "id" in data


def test_register_user_duplicate_email(client):
    """Tests that registering with an already existing email returns a conflict error"""
    payload = {
        "email": "duplicate@example.com",
        "full_name": "Test User",
        "password": "strongpassword123"
    }
    response1 = client.post("/api/v1/auth/register", json=payload)
    assert response1.status_code == 201

    response2 = client.post("/api/v1/auth/register", json=payload)
    assert response2.status_code == 409
    data = response2.json()
    assert "error" in data
    assert data["error"]["code"] == "CONFLICT"


def test_login_access_token_success(client, db):
    """Tests successful login with username and password"""
    # Pre-create user in database
    user_in = UserCreate(
        email="loginuser@example.com",
        full_name="Login User",
        password="correctpassword",
        role=UserRole.BUSINESS_USER
    )
    user_repository.create(db, obj_in=user_in)

    login_payload = {
        "username": "loginuser@example.com",
        "password": "correctpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_access_token_incorrect_password(client, db):
    """Tests that logging in with incorrect credentials returns unauthorized"""
    user_in = UserCreate(
        email="wrongpass@example.com",
        full_name="User",
        password="correctpassword"
    )
    user_repository.create(db, obj_in=user_in)

    login_payload = {
        "username": "wrongpass@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_payload)
    assert response.status_code == 401


def test_get_current_user_profile_me(client, db):
    """Tests retrieving profile using JWT token"""
    user_in = UserCreate(
        email="me@example.com",
        full_name="Me User",
        password="mypassword",
        role=UserRole.BUSINESS_USER
    )
    user = user_repository.create(db, obj_in=user_in)

    # Login to obtain token
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "me@example.com", "password": "mypassword"}
    )
    token = login_response.json()["access_token"]

    # Request /me profile details
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["id"] == user.id


def test_rbac_permissions(client, db):
    """Tests role-based access control restrictions on endpoints"""
    # 1. Create an admin user
    admin_in = UserCreate(
        email="admin@example.com",
        full_name="Admin User",
        password="adminpassword",
        role=UserRole.ADMIN
    )
    user_repository.create(db, obj_in=admin_in)

    # 2. Create an analyst user
    analyst_in = UserCreate(
        email="analyst@example.com",
        full_name="Analyst User",
        password="analystpassword",
        role=UserRole.ANALYST
    )
    user_repository.create(db, obj_in=analyst_in)

    # Logins
    login_admin = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@example.com", "password": "adminpassword"}
    )
    admin_token = login_admin.json()["access_token"]

    login_analyst = client.post(
        "/api/v1/auth/login",
        data={"username": "analyst@example.com", "password": "analystpassword"}
    )
    analyst_token = login_analyst.json()["access_token"]

    # Test Admin route with Admin user -> should succeed
    response = client.get(
        "/api/v1/test-admin-only",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    # Test Admin route with Analyst user -> should fail (403)
    response = client.get(
        "/api/v1/test-admin-only",
        headers={"Authorization": f"Bearer {analyst_token}"}
    )
    assert response.status_code == 403

    # Test Analyst route with Admin user -> should succeed (since admin is allowed)
    response = client.get(
        "/api/v1/test-analyst-only",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    # Test Analyst route with Analyst user -> should succeed
    response = client.get(
        "/api/v1/test-analyst-only",
        headers={"Authorization": f"Bearer {analyst_token}"}
    )
    assert response.status_code == 200


def test_google_oauth_mock_login(client):
    """Tests mock google oauth registration and login flow"""
    google_payload = {
        "id_token": "mock_google_user"
    }
    response = client.post("/api/v1/auth/google-login", json=google_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Confirm the new user is created and accessible via /me
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    profile_response = client.get("/api/v1/auth/me", headers=headers)
    assert profile_response.status_code == 200
    profile_data = profile_response.json()
    assert profile_data["email"] == "google_user@example.com"
    assert profile_data["full_name"] == "Google User"
