from sqlalchemy import Column, Integer, Float, String, Text, ARRAY, TIMESTAMP, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Engine and session for HostData and JobData models
HOST_AND_JOB_DATA_ENGINE_URL = f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPW')}@{os.getenv('DBHOST')}/{os.getenv('DBNAME')}"
host_and_data_table_engine = create_engine(HOST_AND_JOB_DATA_ENGINE_URL)  # add echo=True to help debugging
SessionLocalHostJob = sessionmaker(autocommit=False, autoflush=False, bind=host_and_data_table_engine)

# Engine and session for ApiUser model
API_USER_ENGINE_URL = f"postgresql://{os.getenv('DBUSER_API')}:{os.getenv('DBPW_API')}@{os.getenv('DBHOST')}/{os.getenv('DBNAME')}"
api_user_table_engine = create_engine(API_USER_ENGINE_URL)  # add echo=True to help debugging
SessionLocalApiUser = sessionmaker(autocommit=False, autoflush=False, bind=api_user_table_engine)


class HostData(Base):
    __tablename__ = 'host_data'

    time = Column(TIMESTAMP, nullable=False, primary_key=True)
    host = Column(String(64), nullable=False)
    jid = Column(String(32), nullable=False)
    type = Column(String(32))
    event = Column(String(64), nullable=False)
    unit = Column(String(16), nullable=False)
    value = Column(Float, nullable=False)
    diff = Column(Float)
    arc = Column(Float)


class JobData(Base):
    __tablename__ = 'job_data'

    jid = Column(String(32))
    submit_time = Column(TIMESTAMP, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False, primary_key=True)
    end_time = Column(TIMESTAMP, nullable=False)
    runtime = Column(Float)
    timelimit = Column(Float)
    node_hrs = Column(Float)
    nhosts = Column(Integer)
    ncores = Column(Integer)
    ngpus = Column(Integer)
    username = Column(String(64), nullable=False)
    account = Column(String(64))
    queue = Column(String(64))
    state = Column(String(64))
    jobname = Column(Text)
    exitcode = Column(Text)
    host_list = Column(ARRAY(String))


class ApiUser(Base):
    __tablename__ = 'api_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP)
    last_login = Column(TIMESTAMP)
