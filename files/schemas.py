from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


# Pydantic model for HostData
class HostData(BaseModel):
    time: datetime
    host: str
    jid: str
    type: Optional[str] = None
    event: str
    unit: str
    value: float
    diff: Optional[float] = None
    arc: Optional[float] = None

    class Config:
        from_attributes= True


# Pydantic model for JobData
class JobData(BaseModel):
    jid: str
    submit_time: datetime
    start_time: datetime
    end_time: datetime
    runtime: Optional[float] = None
    timelimit: Optional[float] = None
    node_hrs: Optional[float] = None
    nhosts: Optional[int] = None
    ncores: Optional[int] = None
    ngpus: Optional[int] = None
    username: str
    account: Optional[str] = None
    queue: Optional[str] = None
    state: Optional[str] = None
    jobname: Optional[str] = None
    exitcode: Optional[str] = None
    host_list: Optional[List[str]] = None

    class Config:
        from_attributes = True
