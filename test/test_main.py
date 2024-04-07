import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock
from typing import Tuple
from datetime import timedelta
import security

from main import app, get_db_host_job_tables, get_db_api_user, get_db_and_user, login, read_job_data_single_jid, \
    read_job_data_single_user, read_job_data_single_job_name, read_job_data_single_host, read_job_data_single_account, \
    read_job_data_single_exit_code, read_host_data_single_jid, read_host_data_single_node
from models import Base, ApiUser
from security import create_access_token
import crud

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def override_get_db_host_job_tables():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_db_api_user():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db_host_job_tables] = override_get_db_host_job_tables
app.dependency_overrides[get_db_api_user] = override_get_db_api_user


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_login(test_db):
    # Create a test user
    password = "test_password"
    hashed_password = security.get_password_hash(password)
    user = ApiUser(username="test_user", password_hash=hashed_password)
    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    # Test successful login
    response = client.post("/token", data={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Test invalid username
    response = client.post("/token", data={"username": "invalid_user", "password": "test_password"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

    # Test invalid password
    response = client.post("/token", data={"username": "test_user", "password": "invalid_password"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_read_job_data_single_jid(test_db):
    # Create a test user and generate an access token
    password = "test_password"
    hashed_password = security.get_password_hash(password)
    user = ApiUser(username="test_user", password_hash=hashed_password)
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))

    # Mock the crud.get_job_data_by_id function
    job_data = [MagicMock()]
    with patch.object(crud, "get_job_data_by_id", return_value=job_data):
        # Test successful retrieval of job data
        response = client.get("/job_data_job_id/test_job_id", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == job_data

        # Test job ID not found
        with patch.object(crud, "get_job_data_by_id", return_value=None):
            response = client.get("/job_data_job_id/invalid_job_id",
                                  headers={"Authorization": f"Bearer {access_token}"})
            assert response.status_code == 404
            assert response.json()["detail"] == "Job ID invalid_job_id not found"


def test_read_job_data_single_user(test_db):
    # Create a test user and generate an access token
    password = "test_password"
    hashed_password = security.get_password_hash(password)
    user = ApiUser(username="test_user", password_hash=hashed_password)
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))

    # Mock the crud.get_job_data_by_user function
    job_data = [MagicMock()]
    with patch.object(crud, "get_job_data_by_user", return_value=job_data):
        # Test successful retrieval of job data
        response = client.get("/job_data_user_id/test_user_id", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == job_data

        # Test user ID not found
        with patch.object(crud, "get_job_data_by_user", return_value=[]):
            response = client.get("/job_data_user_id/invalid_user_id",
                                  headers={"Authorization": f"Bearer {access_token}"})
            assert response.status_code == 404
            assert response.json()["detail"] == "User ID invalid_user_id not found"


def test_read_job_data_single_job_name(test_db):
    # Create a test user and generate an access token
    password = "test_password"
    hashed_password = security.get_password_hash(password)
    user = ApiUser(username="test_user", password_hash=hashed_password)
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))

    # Mock the crud.get_job_data_by_job_name function
    job_data = [MagicMock()]
    with patch.object(crud, "get_job_data_by_job_name", return_value=job_data):
        # Test successful retrieval of job data
        response = client.get("/job_data_job_name/test_job_name", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == job_data

        # Test job name not found
        with patch.object(crud, "get_job_data_by_job_name", return_value=[]):
            response = client.get("/job_data_job_name/invalid_job_name",
                                  headers={"Authorization": f"Bearer {access_token}"})
            assert response.status_code == 404
            assert response.json()["detail"] == "Job name invalid_job_name not found"


def test_read_job_data_single_host(test_db):
    # Create a test user and generate an access token
    password = "test_password"
    hashed_password = security.get_password_hash(password)
    user = ApiUser(username="test_user", password_hash=hashed_password)
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))

    # Mock the crud.get_job_data_by_host_id function
    job_data = [MagicMock()]
    with patch.object(crud, "get_job_data_by_host_id", return_value=job_data):
        # Test successful retrieval of job data
        response = client.get("/job_data_host_id/test_host_id", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == job_data

        # Test host ID not found
        with patch.object(crud, "get_job_data_by_host_id", return_value=[]):
            response = client.get("/job_data_host_id/invalid_host_id",
                                  headers={"Authorization": f"Bearer {access_token}"})
            assert response.status_code == 404
            assert response.json()["detail"] == "Host ID invalid_host_id not found"


def test_read_job_data_single_account(test_db):
    # Create a test user and generate an access token
    password = "test_password"
    hashed_password = security.get_password_hash(password)
    user = ApiUser(username="test_user", password_hash=hashed_password)
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))

    # Mock the crud.get_job_data_by_account function
    job_data = [MagicMock()]
    with patch.object(crud, "get_job_data_by_account", return_value=job_data):
        # Test successful retrieval of job data
        response = client.get("/job_data_account_id/test_account_id",
                              headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == job_data

        # Test account ID not found
        with patch.object(crud, "get_job_data_by_account", return_value=[]):
            response = client.get("/job_data_account_id/invalid_account_id",
                                  headers={"Authorization": f"Bearer {access_token}"})
            assert response.status_code == 404
            assert response.json()["detail"] == "Account ID invalid_account_id not found"


def test_read_job_data_single_exit_code(test_db):
    # Create a test user and generate an access token
    password = "test_password"
    hashed_password = security.get_password_hash(password)
    user = ApiUser(username="test_user", password_hash=hashed_password)
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))

    # Mock the crud.get_job_data_by_exit_code function
    job_data = [MagicMock()]
    with patch.object(crud, "get_job_data_by_exit_code", return_value=job_data):
        # Test successful retrieval of job data
        response = client.get("/job_data_exit_code/test_exit_code", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == job_data

        # Test exit code not found
        with patch.object(crud, "get_job_data_by_exit_code", return_value=[]):
            response = client.get("/job_data_exit_code/invalid_exit_code",
                                  headers={"Authorization": f"Bearer {access_token}"})
            assert response.status_code == 404
            assert response.json()["detail"] == "Exit code invalid_exit_code not found"


def test_read_host_data_single_jid(test_db):
    # Create a test user and generate an access token
    password = "test_password"
    hashed_password = security.get_password_hash(password)
    user = ApiUser(username="test_user", password_hash=hashed_password)
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))

    # Mock the crud.get_host_data_by_job_id function
    host_data = [MagicMock()]
    with patch.object(crud, "get_host_data_by_job_id", return_value=host_data):
        # Test successful retrieval of host data
        response = client.get("/host_data_job_id/test_job_data_id", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == host_data

        # Test job data ID not found
        with patch.object(crud, "get_host_data_by_job_id", return_value=[]):
            response = client.get("/host_data_job_id/invalid_job_data_id",
                                  headers={"Authorization": f"Bearer {access_token}"})
            assert response.status_code == 404
            assert response.json()["detail"] == "Host data for job ID invalid_job_data_id not found"


def test_read_host_data_single_node(test_db):
    # Create a test user and generate an access token
    password = "test_password"
    hashed_password = security.get_password_hash(password)
    user = ApiUser(username="test_user", password_hash=hashed_password)
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))

    # Mock the crud.get_host_data_by_host_id function
    host_data = [MagicMock()]
    with patch.object(crud, "get_host_data_by_host_id", return_value=host_data):
        # Test successful retrieval of host data
        response = client.get("/host_data_node_id/test_node_id", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == host_data

        # Test node ID not found
        with patch.object(crud, "get_host_data_by_host_id", return_value=[]):
            response = client.get("/host_data_node_id/invalid_node_id",
                                  headers={"Authorization": f"Bearer {access_token}"})
            assert response.status_code == 404
            assert response.json()["detail"] == "Host data for node invalid_node_id not found"
