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
    return db.query(models.HostData).filter(models.HostData.host == host_id).limit(row_limit).all()


def get_host_data_by_job_id(db: Session, job_data_id: str, row_limit: int = 100):
    """
    Retrieve a list of 'HostData' records from the 'host_data' table filtered by a job identifier, with an optional row limit.

    This function performs a query on the 'host_data' table using SQLAlchemy, filtering by the job data identifier ('jid'). It
    returns a list of 'HostData' objects that correspond to the provided job identifier. The function supports limiting the
    number of records returned via the 'row_limit' parameter. If no records are found matching the job identifier, an empty
    list is returned.

    Parameters:
    :param: db (Session): An instance of the SQLAlchemy Session. This session is used to perform the database query.
                         The session acts as the 'staging zone' for all objects loaded into the database session.
    :param: job_data_id (str): The job identifier used to filter the records in the 'host_data' table. This is typically a
                              unique identifier associated with a specific job or task.
    :param: row_limit (int, optional): The maximum number of records to return. Defaults to 100 if not specified.

    :return: List[HostData]: A list of 'HostData' objects representing the fetched records from the 'host_data' table.
                             The list may be empty if no matching records are found.

    Usage example:
    # Fetch host data records by a specific job ID with a limit of 50 rows
    host_data_for_job = get_host_data_by_job_id(db_session, job_data_id="JOB123", row_limit=50)
    """
    return db.query(models.HostData).filter(models.HostData.jid == job_data_id).limit(row_limit).all()


def get_host_data_by_datetime(db: Session, time_input: str, row_limit: int = 100):
    # Convert the string to a datetime object
    date_obj = datetime.strptime(time_input, "%m-%d-%Y")

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

    :param:: db (Session): The database session to use for the query.
    :param:: job_data_id (str): The job identifier to filter the records.

    :return: List[JobData]: A list of JobData records matching the given jid.
    """
    return db.query(models.JobData).filter(models.JobData.jid == job_data_id).limit(row_limit).all()


def get_job_data_by_user(db: Session, user_id: str, row_limit: int = 100):
    """
    Retrieve a list of 'JobData' records from the 'job_data' table filtered by a user identifier, with an optional row limit.

    This function performs a query on the 'job_data' table using SQLAlchemy, filtering by the user identifier. It returns
    a list of 'JobData' objects that correspond to the provided user identifier. The function supports limiting the number
    of records returned via the 'row_limit' parameter. If no records are found matching the user identifier, an empty list
    is returned.

    Parameters:
    :param: db (Session): An instance of the SQLAlchemy Session. This session is used to perform the database query.
                         The session acts as the 'staging zone' for all objects loaded into the database session.
    :param: user_id (str): The user identifier used to filter the records in the 'job_data' table. This is typically a
                          unique identifier associated with a specific user.
    :param: row_limit (int, optional): The maximum number of records to return. Defaults to 100 if not specified.

    :return: List[JobData]: A list of 'JobData' objects representing the fetched records from the 'job_data' table.
                             The list may be empty if no matching records are found.

    Usage example:
    # Fetch job data records by a specific user ID with a limit of 50 rows
    job_data_for_user = get_job_data_by_user(db_session, user_id="user123", row_limit=50)
    """
    return db.query(models.JobData).filter(models.JobData.username == user_id).limit(row_limit).all()


def get_job_data_by_job_name(db: Session, job_name: str, row_limit: int = 100):
    """
    Retrieve a list of 'JobData' records from the 'job_data' table filtered by a job name, with an optional row limit.

    This function performs a query on the 'job_data' table using SQLAlchemy, filtering by the job name. It returns
    a list of 'JobData' objects that correspond to the provided job name. The function supports limiting the number
    of records returned via the 'row_limit' parameter. If no records are found matching the job name, an empty list
    is returned.

    Parameters:
    :param: db (Session): An instance of the SQLAlchemy Session. This session is used to perform the database query.
                         The session acts as the 'staging zone' for all objects loaded into the database session.
    :param: job_name (str): The job name used to filter the records in the 'job_data' table. This can be a name or title
                           associated with a specific job or task.
    :param: row_limit (int, optional): The maximum number of records to return. Defaults to 100 if not specified.

    :return: List[JobData]: A list of 'JobData' objects representing the fetched records from the 'job_data' table.
                             The list may be empty if no matching records are found.

    Usage example:
    # Fetch job data records by a specific job name with a limit of 50 rows
    job_data_for_job_name = get_job_data_by_job_name(db_session, job_name="ExampleJob", row_limit=50)
    """
    return db.query(models.JobData).filter(models.JobData.jobname == job_name).limit(row_limit).all()


def get_job_data_by_host_id(db: Session, host_id: str, row_limit: int = 100):
    """
    Retrieve a list of 'JobData' records from the 'job_data' table filtered by a host identifier, with an optional row limit.

    This function performs a query on the 'job_data' table using SQLAlchemy, filtering by a specified host identifier.
    It returns a list of 'JobData' objects that are associated with the provided host identifier. The function allows
    specifying a maximum number of records to return through the 'row_limit' parameter. If no records are found that
    match the host identifier, an empty list is returned.

    Parameters:
    :param: db (Session): An instance of the SQLAlchemy Session. This session is used to perform the database query.
                         The session acts as the 'staging zone' for all objects loaded into the database session.
    :param: host_id (str): The host identifier used to filter the records in the 'job_data' table. This identifier
                          typically corresponds to a unique identifier associated with a specific host.
    :param: row_limit (int, optional): The maximum number of records to return. Defaults to 100 if not specified.

    :return: List[JobData]: A list of 'JobData' objects representing the fetched records from the 'job_data' table.
                             The list may be empty if no matching records are found.

    Usage example:
    # Fetch job data records by a specific host ID with a limit of 50 rows
    job_data_for_host = get_job_data_by_host_id(db_session, host_id="host123", row_limit=50)
    """
    return db.query(models.JobData).filter(models.JobData.host_list.any(host_id)).limit(row_limit).all()


def get_job_data_by_account(db: Session, account_id: str, row_limit: int = 100):
    """
    Retrieve a list of 'JobData' records from the 'job_data' table filtered by an account identifier, with an optional row limit.

    This function performs a query on the 'job_data' table using SQLAlchemy, filtering by the account identifier. It returns
    a list of 'JobData' objects that correspond to the provided account identifier. The function supports limiting the number
    of records returned via the 'row_limit' parameter. If no records are found matching the account identifier, an empty list
    is returned.

    Parameters:
    :param: db (Session): An instance of the SQLAlchemy Session. This session is used to perform the database query.
                         The session acts as the 'staging zone' for all objects loaded into the database session.
    :param: account_id (str): The account identifier used to filter the records in the 'job_data' table. This is typically a
                             unique identifier associated with a specific account.
    :param: row_limit (int, optional): The maximum number of records to return. Defaults to 100 if not specified.

    :return: List[JobData]: A list of 'JobData' objects representing the fetched records from the 'job_data' table.
                             The list may be empty if no matching records are found.

    Usage example:
    # Fetch job data records by a specific account ID with a limit of 50 rows
    job_data_for_account = get_job_data_by_account(db_session, account_id="account456", row_limit=50)
    """
    return db.query(models.JobData).filter(models.JobData.account == account_id).limit(row_limit).all()


def get_job_data_by_exit_code(db: Session, exit_code: str, row_limit: int = 100):
    """
    Retrieve a list of 'JobData' records from the 'job_data' table filtered by an exit code, with an optional row limit.

    This function performs a query on the 'job_data' table using SQLAlchemy, filtering by the specified exit code. It returns
    a list of 'JobData' objects that match the provided exit code. The function allows setting a maximum number of records
    to be returned through the 'row_limit' parameter. If no records are found that match the exit code, an empty list
    is returned.

    Parameters:
    :param: db (Session): An instance of the SQLAlchemy Session. This session is used to perform the database query.
                         The session acts as the 'staging zone' for all objects loaded into the database session.
    :param: exit_code (str): The exit code used to filter the records in the 'job_data' table. This code typically represents
                            the status or result code from a job or process execution.
    :param: row_limit (int, optional): The maximum number of records to return. Defaults to 100 if not specified.

    :return: List[JobData]: A list of 'JobData' objects representing the fetched records from the 'job_data' table.
                             The list may be empty if no matching records are found.

    Usage example:
    # Fetch job data records by a specific exit code with a limit of 50 rows
    job_data_for_exit_code = get_job_data_by_exit_code(db_session, exit_code="0", row_limit=50)
    """
    return db.query(models.JobData).filter(models.JobData.exitcode == exit_code).limit(row_limit).all()
