from typing import List, Tuple
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.orm import Session
import crud
import models
import schemas
import security
from models import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
ROW_LIMIT = 300


# -------------- helpers -------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_and_user(db: Session = Depends(get_db),
                    current_user: models.ApiUser = Depends(security.get_current_active_user)):
    return db, current_user


# -------------- authorization endpoint -------------------------------------------------------------

@app.post("/token", response_model=security.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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


# -------------- job data endpoints -------------------------------------------------------------


@app.get("/job_data_job_id/{job_id}", response_model=List[schemas.JobData])
def read_job_data_single_jid(job_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    db_items = crud.get_job_data_by_id(db, job_data_id=job_id, row_limit=ROW_LIMIT)
    if not db_items:
        raise HTTPException(status_code=404, detail=f"{job_id} not found")
    return db_items


@app.get("/job_data_user_id/{user_id}", response_model=List[schemas.JobData])
def read_job_data_single_user(user_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    db_items = crud.get_job_data_by_user(db, user_id=user_id, row_limit=ROW_LIMIT)
    if not db_items:
        raise HTTPException(status_code=404, detail=f"{user_id} not found")
    return db_items


@app.get("/job_data_job_name/{job_name}", response_model=List[schemas.JobData])
def read_job_data_single_job_name(job_name: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    db_items = crud.get_job_data_by_job_name(db, job_name=job_name, row_limit=ROW_LIMIT)
    if not db_items:
        raise HTTPException(status_code=404, detail=f"{job_name} not found")
    return db_items


@app.get("/job_data_host_id/{host_id}", response_model=List[schemas.JobData])
def read_job_data_single_host(host_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    db_items = crud.get_job_data_by_host_id(db, host_id=host_id, row_limit=ROW_LIMIT)
    if not db_items:
        raise HTTPException(status_code=404, detail=f"{host_id} not found")
    return db_items


@app.get("/job_data_account_id/{account_id}", response_model=List[schemas.JobData])
def read_job_data_single_account(account_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    db_items = crud.get_job_data_by_account(db, account_id=account_id, row_limit=ROW_LIMIT)
    if not db_items:
        raise HTTPException(status_code=404, detail=f"{account_id} not found")
    return db_items


@app.get("/job_data_exit_code/{exit_code}", response_model=List[schemas.JobData])
def read_job_data_single_exit_code(exit_code: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    db_items = crud.get_job_data_by_exit_code(db, exit_code=exit_code, row_limit=ROW_LIMIT)
    if not db_items:
        raise HTTPException(status_code=404, detail=f"{exit_code} not found")
    return db_items


# -------------- host data endpoints -------------------------------------------------------------

@app.get("/host_data_job_id/{job_data_id}", response_model=List[schemas.HostData])
def read_host_data_single_jid(job_data_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    db_items = crud.get_host_data_by_job_id(db, job_data_id=job_data_id, row_limit=ROW_LIMIT)
    if not db_items:
        raise HTTPException(status_code=404, detail=f"{job_data_id} not found")
    return db_items


@app.get("/host_data_node_id/{node_id}", response_model=List[schemas.HostData])
def read_host_data_single_node(node_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    print("calling get_host_data_by_host_id")
    db_items = crud.get_host_data_by_host_id(db, host_id=node_id, row_limit=ROW_LIMIT)
    if not db_items:
        raise HTTPException(status_code=404, detail=f"{node_id} not found")
    return db_items


@app.get("/host_data_datetime/{time_input}", response_model=List[schemas.HostData])  # TODO - fix
def read_host_data_by_datetime(time_input: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    db_items = crud.get_host_data_by_datetime(db, time_input=time_input, row_limit=ROW_LIMIT)
    if not db_items:
        raise HTTPException(status_code=404, detail=f"{time_input} not found")
    return db_items
