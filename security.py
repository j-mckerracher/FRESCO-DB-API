from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.testing.pickleable import User
from jwt import PyJWTError
import jwt
import models
import os


SECRET_KEY = os.environ["FASTAPI_SECURITY_KEY"]
ALGORITHM = os.environ["FASTAPI_SECURITY_KEY_ALGO"]
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_db_api_user():
    """
    Create and manage a database session for API user models.

    This function initializes a database session using the `SessionLocalApiUser` method from the `models` module,
    specifically for interactions with the API user data models. It is designed to be used as a context manager,
    ensuring that the database session is properly opened and closed. The function yields the database session to
    the caller and ensures that the session is closed properly, regardless of whether an exception occurs or not.

    This function is typically used in a 'with' statement or in a dependency injection scenario in a web framework
    like FastAPI to provide a session for a single request/response cycle.

    Yields:
    :yield: Session: The SQLAlchemy Session object for API user database transactions.

    Usage example:
    # Using the function with a 'with' statement
    with get_db_api_user() as db:
        # Perform database operations using 'db'
        pass
    """
    db = models.SessionLocalApiUser()
    try:
        yield db
    finally:
        db.close()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """
    Verify a plaintext password against a hashed password.

    This function uses a password context to verify if a given plaintext password matches a hashed password.
    It is commonly used in scenarios where user authentication is required, such as login processes. The function
    relies on the 'pwd_context' object, which should be configured with the desired hashing algorithm.

    Parameters:
    :param: plain_password (str): The plaintext password that needs to be verified.
    :param: hashed_password (str): The hashed password against which the plaintext password will be verified.

    :return: bool: Returns True if the plaintext password matches the hashed password, otherwise False.

    Usage example:
    # Verifying a user's password during login
    is_password_correct = verify_password(user_input_password, stored_hashed_password)
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Generate a hashed version of a plaintext password.

    This function takes a plaintext password and uses the 'pwd_context' object to create a hashed version of it.
    The 'pwd_context' should be set up with a specific hashing algorithm (e.g., bcrypt, Argon2). Hashing passwords
    is a crucial security measure for safely storing user passwords. Instead of storing the plaintext passwords,
    only the hashes are stored, and these hashes are checked during user authentication.

    Parameters:
    :param: password (str): The plaintext password that needs to be hashed.

    :return: str: The hashed version of the provided plaintext password.

    Usage example:
    # Hashing a new user's password for storage
    hashed_password = get_password_hash(new_user_password)
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT (JSON Web Token) access token with an optional expiration time.

    This function generates an access token using the provided data and an optional expiration time delta. If no expiration
    time delta is provided, a default of 15 minutes is used. The token is encoded with a specified secret key (SECRET_KEY)
    and algorithm (ALGORITHM). JWTs are typically used in authentication and authorization processes to securely transmit
    information between parties.

    Parameters:
    :param: data (dict): The data to be encoded into the JWT. This often includes user identity information.
    :param: expires_delta (Optional[timedelta], optional): The time delta for the token's expiration. Defaults to 15 minutes if not provided.

    :return: str: The encoded JWT access token.

    Usage example:
    # Creating an access token for a user with a specific expiration time
    access_token = create_access_token(data={"sub": user_id}, expires_delta=timedelta(hours=1))
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db: Session, username: str):
    """
    Retrieve a single user record from the 'ApiUser' table by a username.

    This function queries the 'ApiUser' table in the database using SQLAlchemy, filtering by the provided username. It
    returns the first 'ApiUser' object that matches the username, if such a record exists. If no matching user is found,
    the function returns None. This is commonly used in user management systems to fetch user details based on their
    username.

    Parameters:
    :param: db (Session): An instance of the SQLAlchemy Session. This session is used to perform the database query.
    :param: username (str): The username of the user to be retrieved.

    :return: ApiUser or None: An 'ApiUser' object representing the user record if found, otherwise None.

    Usage example:
    # Retrieve a user record by username
    user = get_user(db_session, username="johndoe")
    """
    return db.query(models.ApiUser).filter(models.ApiUser.username == username).first()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_api_user)):
    """
    Asynchronously retrieve the current user based on a provided JWT access token.

    This coroutine function decodes a JWT access token to extract the username (subject) and then retrieves the corresponding
    user record from the database. It requires a valid token passed as a Bearer token in the request's authorization header.
    If the token is invalid, expired, or if the user does not exist in the database, it raises an HTTP 401 Unauthorized exception.
    This function is typically used in web applications (e.g., with FastAPI) to authenticate and identify a user making a request.

    Parameters:
    :param: token (str): The JWT access token, obtained via dependency injection using `oauth2_scheme`.
    :param: db (Session): An instance of the SQLAlchemy Session, obtained via dependency injection using `get_db_api_user`.

    Raises:
    :raises HTTPException: An exception with status code 401 (Unauthorized) if the token is invalid or the user does not exist.

    Returns:
    :returns: The user object corresponding to the username extracted from the token.

    Usage example:
    # This function is typically used as a dependency in FastAPI route handlers
    @app.get("/users/me")
    async def read_users_me(current_user: models.ApiUser = Depends(get_current_user)):
        return current_user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user
    except PyJWTError:
        raise credentials_exception


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Asynchronously retrieve the currently active user.

    This coroutine function is a wrapper around `get_current_user`. It directly returns the user object obtained from
    `get_current_user`, which is typically an authenticated user's data. This function can be used in scenarios where
    you need to ensure that there is an active, authenticated user making a request, such as in protected routes in
    web applications.

    Parameters:
    :param: current_user (User): The user object, obtained via dependency injection using `get_current_user`.

    Returns:
    :returns: The currently authenticated and active user object.

    Usage example:
    # This function is usually used as a dependency in FastAPI route handlers
    @app.get("/users/profile")
    async def read_user_profile(active_user: User = Depends(get_current_active_user)):
        return active_user
    """
    return current_user
