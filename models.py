from sqlalchemy import Column, Integer, Float, String, Text, ARRAY, TIMESTAMP, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPW')}@{os.getenv('DBHOST')}/{os.getenv('DBNAME')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


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
    host_list = Column(ARRAY(Text))


class ApiUser(Base):
    __tablename__ = 'api_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP)
    last_login = Column(TIMESTAMP)
