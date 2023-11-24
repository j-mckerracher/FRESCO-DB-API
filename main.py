from typing import List, Tuple
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.orm import Session
import crud
import models
import schemas
import security
from models import SessionLocalHostJob, host_and_data_table_engine
from fastapi.security import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=host_and_data_table_engine)
app = FastAPI()
ROW_LIMIT = 300


# -------------- helpers -------------------------------------------------------------

def get_db_host_job_tables():
    """
    Provides a database session for a single request, and closes it afterwards.

    Yields a SQLAlchemy SessionLocal instance that is used for database operations. The session is
    closed once the request is complete.

    :yield: A SQLAlchemy SessionLocal instance for database operations.
    :raises HTTPException: If an error occurs during session creation or closure.
    """
    db = SessionLocalHostJob()
    try:
        yield db
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def get_db_and_user(db: Session = Depends(get_db_host_job_tables),
                    current_user: models.ApiUser = Depends(security.get_current_active_user)):
    """
    Retrieve the database session and the current authenticated user.

    :param: db (Session): A dependency that provides access to the database session.
    :param: current_user (models.ApiUser): A dependency that provides the current authenticated user.

    :return: Tuple[Session, models.ApiUser]: A tuple containing the database session and the current authenticated user.
    :raises HTTPException: If there is an error in fetching the database session or the current user.
    """
    try:
        return db, current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------- authorization endpoint -------------------------------------------------------------

@app.post("/token", response_model=security.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_host_job_tables)):
    """
    Authenticate a user and return an access token.

    :param: form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
    :param: db (Session): A database session dependency.

    :return: security.Token: A token response model containing the access token and token type.
    :raises HTTPException: If the username is not found or the password is incorrect.
    """
    try:
        user = security.get_user(db, username=form_data.username)
        if not user or not security.verify_password(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------- job data endpoints -------------------------------------------------------------


@app.get("/job_data_job_id/{job_id}", response_model=List[schemas.JobData])
def read_job_data_single_jid(job_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    """
    Fetch all job data records associated with a given job ID.

    :param: job_id (str): The job identifier used to filter the job data records.
    :param: db_user (Tuple[Session, models.ApiUser]): A tuple containing the database session and the current authenticated user.

    :return: List[schemas.JobData]: A list of JobData records where the job_id matches the specified value.
    :raises HTTPException: If no records are found or if there is a database error.
    """
    db, current_user = db_user
    try:
        db_items = crud.get_job_data_by_id(db, job_data_id=job_id, row_limit=ROW_LIMIT)
        if not db_items:
            raise HTTPException(status_code=404, detail=f"Job ID {job_id} not found")
        return db_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/job_data_user_id/{user_id}", response_model=List[schemas.JobData])
def read_job_data_single_user(user_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    """
    Fetch all job data records associated with a given user ID.

    :param: user_id (str): The user identifier used to filter the job data records.
    :param: db_user (Tuple[Session, models.ApiUser]): A tuple containing the database session and the current authenticated user.

    :return: List[schemas.JobData]: A list of JobData records where the user_id matches the specified value.
    :raises HTTPException: If no records are found or if there is a database error.
    """
    db, current_user = db_user
    try:
        db_items = crud.get_job_data_by_user(db, user_id=user_id, row_limit=ROW_LIMIT)
        if not db_items:
            raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")
        return db_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/job_data_job_name/{job_name}", response_model=List[schemas.JobData])
def read_job_data_single_job_name(job_name: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    """
    Fetch all job data records associated with a given job name.

    :param: job_name (str): The job name used to filter the job data records.
    :param: db_user (Tuple[Session, models.ApiUser]): A tuple containing the database session and the current authenticated user.

    :return: List[schemas.JobData]: A list of JobData records where the job_name matches the specified value.
    :raises HTTPException: If no records are found or if there is a database error.
    """
    db, current_user = db_user
    try:
        db_items = crud.get_job_data_by_job_name(db, job_name=job_name, row_limit=ROW_LIMIT)
        if not db_items:
            raise HTTPException(status_code=404, detail=f"Job name {job_name} not found")
        return db_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/job_data_host_id/{host_id}", response_model=List[schemas.JobData])
def read_job_data_single_host(host_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    """
    Fetch all job data records associated with a given host ID.

    :param: host_id (str): The host identifier used to filter the job data records.
    :param: db_user (Tuple[Session, models.ApiUser]): A tuple containing the database session and the current authenticated user.

    :return: List[schemas.JobData]: A list of JobData records where the host_id is present in the job's host list.
    :raises HTTPException: If no records are found or if there is a database error.
    """
    db, current_user = db_user
    try:
        db_items = crud.get_job_data_by_host_id(db, host_id=host_id, row_limit=ROW_LIMIT)
        if not db_items:
            raise HTTPException(status_code=404, detail=f"Host ID {host_id} not found")
        return db_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/job_data_account_id/{account_id}", response_model=List[schemas.JobData])
def read_job_data_single_account(account_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    """
    Fetch all job data records associated with a given account ID.

    :param: account_id (str): The account identifier used to filter the job data records.
    :param: db_user (Tuple[Session, models.ApiUser]): A tuple containing the database session and the current authenticated user.

    :return: List[schemas.JobData]: A list of JobData records where the account_id matches the specified value.
    :raises HTTPException: If no records are found or if there is a database error.
    """
    db, current_user = db_user
    try:
        db_items = crud.get_job_data_by_account(db, account_id=account_id, row_limit=ROW_LIMIT)
        if not db_items:
            raise HTTPException(status_code=404, detail=f"Account ID {account_id} not found")
        return db_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/job_data_exit_code/{exit_code}", response_model=List[schemas.JobData])
def read_job_data_single_exit_code(exit_code: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    """
    Fetch all job data records associated with a given exit code.

    :param: exit_code (str): The exit code used to filter the job data records.
    :param: db_user (Tuple[Session, models.ApiUser]): A tuple containing the database session and the current authenticated user.

    :return: List[schemas.JobData]: A list of JobData records where the exit_code matches the specified value.
    :raises HTTPException: If no records are found or if there is a database error.
    """
    db, current_user = db_user
    try:
        db_items = crud.get_job_data_by_exit_code(db, exit_code=exit_code, row_limit=ROW_LIMIT)
        if not db_items:
            raise HTTPException(status_code=404, detail=f"Exit code {exit_code} not found")
        return db_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------- host data endpoints -------------------------------------------------------------

@app.get("/host_data_job_id/{job_data_id}", response_model=List[schemas.HostData])
def read_host_data_single_jid(job_data_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    """
    Fetch all host data records associated with a given job data ID.

    :param: job_data_id (str): The job data identifier used to filter the host data records.
    :param: db_user (Tuple[Session, models.ApiUser]): A tuple containing the database session and the current authenticated user.

    :return: List[schemas.HostData]: A list of HostData records where the job_data_id is associated with the job data records.
    :raises HTTPException: If no records are found or if there is a database error.
    """
    db, current_user = db_user
    try:
        db_items = crud.get_host_data_by_job_id(db, job_data_id=job_data_id, row_limit=ROW_LIMIT)
        if not db_items:
            raise HTTPException(status_code=404, detail=f"Host data for job ID {job_data_id} not found")
        return db_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/host_data_node_id/{node_id}", response_model=List[schemas.HostData])
def read_host_data_single_node(node_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    """
    Fetch all host data records associated with a given node ID.

    :param: node_id (str): The node identifier used to filter the host data records.
    :param: db_user (Tuple[Session, models.ApiUser]): A tuple containing the database session and the current authenticated user.

    :return: List[schemas.HostData]: A list of HostData records where the node_id is present in the host list.
    :raises HTTPException: If no records are found or if there is a database error.
    """
    db, current_user = db_user
    try:
        db_items = crud.get_host_data_by_host_id(db, host_id=node_id, row_limit=ROW_LIMIT)
        if not db_items:
            raise HTTPException(status_code=404, detail=f"Host data for node {node_id} not found")
        return db_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
