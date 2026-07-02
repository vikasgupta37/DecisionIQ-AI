import io
import json
import os
import shutil
from backend.app.crud.user import user_repository
from backend.app.models.user import UserRole
from backend.app.schemas.user import UserCreate


def _create_user_and_get_token(client, db, email="uploader@example.com"):
    """Helper to create a user and return the JWT token."""
    user_in = UserCreate(
        email=email,
        full_name="Upload Tester",
        password="password123",
        role=UserRole.BUSINESS_USER,
    )
    user = user_repository.create(db, obj_in=user_in)
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    return user, {"Authorization": f"Bearer {token}"}


def test_upload_requires_auth(client):
    """Uploading without a JWT token must return 401."""
    fake_file = io.BytesIO(b"a,b,c\n1,2,3")
    response = client.post(
        "/api/v1/upload",
        files={"file": ("data.csv", fake_file, "text/csv")},
    )
    assert response.status_code == 401


def test_upload_csv_success(client, db):
    """Tests successful CSV file upload with metadata extraction."""
    user, headers = _create_user_and_get_token(client, db)

    csv_content = b"name,age,city\nAlice,30,NYC\nBob,25,SF\nCharlie,35,LA"
    response = client.post(
        "/api/v1/upload",
        files={"file": ("people.csv", io.BytesIO(csv_content), "text/csv")},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()

    # Dataset record checks
    assert data["dataset"]["name"] == "people.csv"
    assert data["dataset"]["file_type"] == "csv"
    assert data["dataset"]["file_size"] == len(csv_content)
    assert data["dataset"]["status"] == "pending"
    assert data["dataset"]["user_id"] == user.id

    # Metadata checks
    assert data["metadata"]["row_count"] == 3
    assert data["metadata"]["column_names"] == ["name", "age", "city"]
    assert "uploaded successfully" in data["message"]

    # Cleanup local file
    _cleanup_uploads()


def test_upload_json_success(client, db):
    """Tests successful JSON file upload with metadata extraction."""
    _, headers = _create_user_and_get_token(client, db, email="jsonuploader@example.com")

    json_data = [
        {"product": "Widget A", "price": 9.99, "qty": 100},
        {"product": "Widget B", "price": 19.99, "qty": 50},
    ]
    json_bytes = json.dumps(json_data).encode("utf-8")

    response = client.post(
        "/api/v1/upload",
        files={"file": ("products.json", io.BytesIO(json_bytes), "application/json")},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()

    assert data["dataset"]["file_type"] == "json"
    assert data["metadata"]["row_count"] == 2
    assert "product" in data["metadata"]["column_names"]
    assert "price" in data["metadata"]["column_names"]

    _cleanup_uploads()


def test_upload_txt_success(client, db):
    """Tests successful TXT file upload with word count."""
    _, headers = _create_user_and_get_token(client, db, email="txtuploader@example.com")

    txt_content = b"Hello World\nThis is a test document\nWith three lines"
    response = client.post(
        "/api/v1/upload",
        files={"file": ("notes.txt", io.BytesIO(txt_content), "text/plain")},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()

    assert data["dataset"]["file_type"] == "txt"
    assert data["metadata"]["word_count"] == 10
    assert data["metadata"]["row_count"] == 3

    _cleanup_uploads()


def test_upload_rejected_unsupported_type(client, db):
    """Tests that uploading an unsupported file type returns 400."""
    _, headers = _create_user_and_get_token(client, db, email="badtype@example.com")

    response = client.post(
        "/api/v1/upload",
        files={"file": ("malware.exe", io.BytesIO(b"MZ..."), "application/octet-stream")},
        headers=headers,
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "INVALID_FILE_TYPE"


def test_upload_rejected_empty_file(client, db):
    """Tests that uploading an empty file returns 400."""
    _, headers = _create_user_and_get_token(client, db, email="empty@example.com")

    response = client.post(
        "/api/v1/upload",
        files={"file": ("empty.csv", io.BytesIO(b""), "text/csv")},
        headers=headers,
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "EMPTY_FILE"


def test_list_datasets_for_user(client, db):
    """Tests listing datasets returns only the current user's uploads."""
    user, headers = _create_user_and_get_token(client, db, email="lister@example.com")

    # Upload two files
    for name in ["file1.csv", "file2.csv"]:
        csv_data = b"col1,col2\nval1,val2"
        client.post(
            "/api/v1/upload",
            files={"file": (name, io.BytesIO(csv_data), "text/csv")},
            headers=headers,
        )

    response = client.get("/api/v1/upload", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["datasets"]) == 2
    # Most recent first
    assert data["datasets"][0]["name"] == "file2.csv"
    assert data["datasets"][1]["name"] == "file1.csv"

    _cleanup_uploads()


def test_get_dataset_by_id(client, db):
    """Tests retrieving a single dataset by its ID."""
    _, headers = _create_user_and_get_token(client, db, email="getter@example.com")

    csv_data = b"x,y\n1,2"
    upload_resp = client.post(
        "/api/v1/upload",
        files={"file": ("single.csv", io.BytesIO(csv_data), "text/csv")},
        headers=headers,
    )
    dataset_id = upload_resp.json()["dataset"]["id"]

    response = client.get(f"/api/v1/upload/{dataset_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "single.csv"

    _cleanup_uploads()


def test_get_dataset_not_found(client, db):
    """Tests that requesting a non-existent dataset returns 404."""
    _, headers = _create_user_and_get_token(client, db, email="notfound@example.com")

    response = client.get("/api/v1/upload/99999", headers=headers)
    assert response.status_code == 404


def _cleanup_uploads():
    """Removes the uploads directory created during tests."""
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")
