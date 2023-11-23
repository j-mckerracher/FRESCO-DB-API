from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models


# ------------------------------- Functions for the host_data table -------------------------------

def get_host_data_by_host_id(db: Session, host_id: str, row_limit: int = 100):
    """
    Retrieve a specific record from the 'host_data' table by its identifier.

    This function performs a query on the 'host_data' table using SQLAlchemy, filtering by the host data identifier.
    It returns a single 'HostData' object that corresponds to the provided identifier. If no record is found
    matching the identifier, it returns None.

    Parameters:
    :param: db (Session): An instance of the SQLAlchemy Session. This session is used to perform the database query.
                         The session acts as the 'staging zone' for all objects loaded into the database session.
    :param: host_data_id (int): The unique identifier of the host data record to be retrieved. This typically corresponds
                               to the primary key in the 'host_data' table.

    :return: HostData or None: A 'HostData' object representing the fetched record from the 'host_data' table if found,
                              otherwise None.

    Usage example:
    # Fetch a specific host data record by its ID
    specific_host_data = get_host_data_by_id(db_session, host_id=NODE2)
    """
    print(f"In get_host_data_by_host_id - querying for {host_id}")
    return db.query(models.HostData).filter(models.HostData.host == host_id).limit(row_limit).all()


def get_host_data_by_job_id(db: Session, job_data_id: str, row_limit: int = 100):
    return db.query(models.HostData).filter(models.HostData.jid == job_data_id).limit(row_limit).all()


def get_host_data_by_datetime(db: Session, time_input: str, row_limit: int = 100):
    # Convert the string to a datetime object
    date_obj = datetime.strptime(time_input, "%m-%d-%Y")

    print(f"date = {date_obj}")

    # Filter using the date part only
    # Assuming models.HostData.time is a DateTime field
    return db.query(models.HostData).filter(
        models.HostData.time >= date_obj,
        models.HostData.time < date_obj + timedelta(days=1)
    ).limit(row_limit).all()


# ------------------------------- Functions for the job_data table -------------------------------


def get_job_data_by_id(db: Session, job_data_id: str, row_limit: int = 100):
    """
    Fetch all job data records with a given job identifier (jid).

    Args:
    db (Session): The database session to use for the query.
    job_data_id (str): The job identifier to filter the records.

    Returns:
    List[JobData]: A list of JobData records matching the given jid.
    """
    print(f"in get_job_data_by_id using {job_data_id}")
    return db.query(models.JobData).filter(models.JobData.jid == job_data_id).limit(row_limit).all()


def get_job_data_by_user(db: Session, user_id: str, row_limit: int = 100):
    return db.query(models.JobData).filter(models.JobData.username == user_id).limit(row_limit).all()


def get_job_data_by_job_name(db: Session, job_name: str, row_limit: int = 100):
    return db.query(models.JobData).filter(models.JobData.jobname == job_name).limit(row_limit).all()


def get_job_data_by_host_id(db: Session, host_id: str, row_limit: int = 100):
    print(f"In get_job_data_by_host_id - querying for {host_id}")
    return db.query(models.JobData).filter(models.JobData.host_list.any(host_id)).limit(row_limit).all()


def get_job_data_by_account(db: Session, account_id: str, row_limit: int = 100):
    return db.query(models.JobData).filter(models.JobData.account == account_id).limit(row_limit).all()


def get_job_data_by_exit_code(db: Session, exit_code: str, row_limit: int = 100):
    return db.query(models.JobData).filter(models.JobData.exitcode == exit_code).limit(row_limit).all()
