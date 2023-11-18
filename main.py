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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_and_user(db: Session = Depends(get_db),
                    current_user: models.ApiUser = Depends(security.get_current_active_user)):
    return db, current_user


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


@app.get("/job_data/", response_model=List[schemas.JobData])
def read_job_data_many_jid(skip: int = 0, limit: int = 100,
                           db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    items = crud.get_job_data(db, skip=skip, limit=limit)
    return items


@app.get("/job_data_job_id/{job_data_id}", response_model=List[schemas.JobData])
def read_job_data_single_jid(job_data_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    db_items = crud.get_job_data_by_id(db, job_data_id=job_data_id)
    if not db_items:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_items


@app.get("/host_data_job_id/{job_data_id}", response_model=List[schemas.HostData])
def read_host_data_single_jid(job_data_id: str, db_user: Tuple[Session, models.ApiUser] = Depends(get_db_and_user)):
    db, current_user = db_user
    db_items = crud.get_host_data_by_job_id(db, job_data_id=job_data_id)
    if not db_items:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_items
