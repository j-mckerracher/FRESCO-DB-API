from sqlalchemy.orm import Session
import models


# ------------------------------- Functions for the host_data table -------------------------------

def get_host_data(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a subset of records from the 'host_data' table.

    This function queries the 'host_data' table using SQLAlchemy and returns a list of 'HostData' objects.
    It supports pagination functionality by allowing control over the offset (skip) and the number of
    records (limit) returned. This is particularly useful for applications that require data to be
    displayed in a paginated format.

    Parameters:
    :param: db (Session): An instance of the SQLAlchemy Session, used to perform database queries.
                         The session represents the 'staging zone' for all objects loaded into the database session.
    :param: skip (int, optional): The number of records to skip from the start. Used for pagination. Defaults to 0.
                                 For instance, if skip is 10, the query skips the first 10 records.
    :param: limit (int, optional): The maximum number of records to return from the query. Defaults to 100.
                                  This controls the size of the result set and is useful for limiting the data
                                  fetched from the database, especially in a paginated API.

    :return: List[HostData]: A list of 'HostData' objects representing the records fetched from the 'host_data' table,
                            considering the specified offset (skip) and limit.

    Usage example:
    # Fetch the first 100 records
    host_data_records = get_host_data(db_session)

    # Fetch the next 100 records
    next_host_data_records = get_host_data(db_session, skip=100, limit=100)
    """
    return db.query(models.HostData).offset(skip).limit(limit).all()


def get_host_data_by_id(db: Session, host_data_id: int):
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
    specific_host_data = get_host_data_by_id(db_session, host_data_id=456)
    """
    return db.query(models.HostData).filter(models.HostData.id == host_data_id).first()


# ------------------------------- Functions for the job_data table -------------------------------

def get_job_data(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a subset of records from the 'job_data' table.

    This function queries the 'job_data' table using SQLAlchemy and returns a list of 'JobData' objects.
    It is designed to support pagination by allowing control over the offset (skip) and the number of
    records (limit) returned.

    Parameters:
    :param: db (Session): An instance of the SQLAlchemy Session. This session is used to query the database.
                      It represents the 'staging zone' for all the objects loaded into the database session.
    :param: skip (int, optional): The number of records to skip in the query, used for pagination. Defaults to 0.
                              For example, if skip is 10, the query will skip the first 10 records.
    :param: limit (int, optional): The maximum number of records to return in the query. Defaults to 100.
                               This controls the size of the result set and is useful for limiting the data
                               fetched from the database, particularly in a paginated API.

    :return List[JobData]: A list of 'JobData' objects representing the records fetched from the 'job_data' table,
                       considering the specified offset and limit.

    Usage example:
    # Fetch the first 100 records
    job_data_records = get_job_data(db_session)

    # Fetch the next 100 records
    next_job_data_records = get_job_data(db_session, skip=100, limit=100)
    """
    return db.query(models.JobData).offset(skip).limit(limit).all()


def get_job_data_by_id(db: Session, job_data_id: str):
    """
    Fetch all job data records with a given job identifier (jid).

    Args:
    db (Session): The database session to use for the query.
    job_data_id (str): The job identifier to filter the records.

    Returns:
    List[JobData]: A list of JobData records matching the given jid.
    """
    return db.query(models.JobData).filter(models.JobData.jid == job_data_id).all()


def get_host_data_by_job_id(db: Session, job_data_id: str):
    return db.query(models.HostData).filter(models.HostData.jid == job_data_id).all()

