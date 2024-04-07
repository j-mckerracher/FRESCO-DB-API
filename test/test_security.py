import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from jwt import PyJWTError
import models
from security import (
    verify_password, get_password_hash, create_access_token, get_user,
    get_current_user, get_current_active_user
)


def test_verify_password():
    plain_password = "password123"
    hashed_password = get_password_hash(plain_password)

    assert verify_password(plain_password, hashed_password) == True
    assert verify_password("wrongpassword", hashed_password) == False


def test_get_password_hash():
    plain_password = "password123"
    hashed_password = get_password_hash(plain_password)

    assert isinstance(hashed_password, str)
    assert hashed_password != plain_password


def test_create_access_token():
    data = {"sub": "johndoe"}
    expires_delta = timedelta(minutes=30)

    token = create_access_token(data, expires_delta)

    assert isinstance(token, str)


@patch("your_module.models.SessionLocalApiUser")
def test_get_db_api_user(mock_session_local):
    mock_session = MagicMock(spec=Session)
    mock_session_local.return_value = mock_session

    with patch("your_module.models.SessionLocalApiUser", mock_session_local):
        with get_db_api_user() as db:
            assert db == mock_session

    mock_session.close.assert_called_once()


def test_get_user(db_session):
    user = models.ApiUser(username="johndoe", hashed_password="hashedpassword")
    db_session.add(user)
    db_session.commit()

    retrieved_user = get_user(db_session, "johndoe")
    assert retrieved_user == user

    nonexistent_user = get_user(db_session, "nonexistent")
    assert nonexistent_user is None


@pytest.mark.asyncio
async def test_get_current_user(db_session):
    user = models.ApiUser(username="johndoe", hashed_password="hashedpassword")
    db_session.add(user)
    db_session.commit()

    token = create_access_token({"sub": "johndoe"})

    with patch("your_module.get_db_api_user", return_value=db_session):
        current_user = await get_current_user(token)
        assert current_user == user

    with patch("your_module.get_db_api_user", return_value=db_session):
        with pytest.raises(HTTPException):
            await get_current_user("invalid_token")

    with patch("your_module.get_db_api_user", return_value=db_session):
        with patch("your_module.jwt.decode", side_effect=PyJWTError):
            with pytest.raises(HTTPException):
                await get_current_user(token)


@pytest.mark.asyncio
async def test_get_current_active_user(db_session):
    user = models.ApiUser(username="johndoe", hashed_password="hashedpassword")
    db_session.add(user)
    db_session.commit()

    with patch("your_module.get_current_user", return_value=user):
        current_active_user = await get_current_active_user()
        assert current_active_user == user