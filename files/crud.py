import database_helpers as dbm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ------------------------------- Functions for the host_data table -------------------------------

def get_host_data_by_host_id(host_id: str, row_limit: int = 100):
    """
    Retrieve host data records from the 'host_data' table filtered by the specified host ID.

    This function establishes a database connection, executes a query to fetch records from the 'host_data' table
    where the 'host' column matches the given host_id, and limits the result set to the specified row_limit.
    The records are then converted into model instances before being returned. The function includes logging
    for significant events and error handling.

    :param host_id: The unique identifier of the host for which to retrieve data.
    :param row_limit: The maximum number of records to return. Defaults to 100 if not specified.
    :return: A list of host data model instances corresponding to the fetched records, or None if the database
             connection cannot be established.
    """
    logger.info(f"Fetching host data for host_id: {host_id} with row limit: {row_limit}")

    connection = dbm.get_database_connection()
    if connection is None:
        logger.error("Failed to establish database connection.")
        return None

    query = "SELECT * FROM host_data WHERE host = %s LIMIT %s"
    params = (host_id, row_limit)

    try:
        records = dbm.execute_query(connection, query, params)
        logger.info(f"Successfully executed query. Number of records fetched: {len(records)}")

        # convert records to model instances
        records = dbm.convert_to_model(records, dbm.record_to_host_data)
        return records
    except Exception as e:
        logger.error(f"Error occurred in get_host_data_by_host_id: {e}")
        raise
    finally:
        connection.close()
        logger.info("Database connection closed.")


def get_host_data_by_job_id(job_data_id: str, row_limit: int = 100) -> list:
    """
    Retrieves host data records from the 'host_data' table filtered by the specified job data ID.

    This function connects to the database and performs a query to fetch records from the 'host_data' table
    where the 'jid' column matches the given job_data_id. The number of records returned is limited to the
    specified row_limit. After fetching the records, it converts them into model instances. The function logs
    key events and handles any exceptions that may occur during the process.

    :param job_data_id: The job data ID used to filter the records in the 'host_data' table.
    :param row_limit: The maximum number of records to return. Defaults to 100 if not specified.
    :return: A list of host data model instances corresponding to the fetched records. Returns None if the
             database connection cannot be established.
    """
    logger.info(f"Fetching host data for host_id: {job_data_id} with row limit: {row_limit}")

    connection = dbm.get_database_connection()
    if connection is None:
        logger.error("Failed to establish database connection.")
        return None

    query = "SELECT * FROM host_data WHERE jid = %s LIMIT %s"
    params = (job_data_id, row_limit)

    try:
        records = dbm.execute_query(connection, query, params)
        logger.info(f"Successfully executed query. Number of records fetched: {len(records)}")

        # convert records to model instances
        records = dbm.convert_to_model(records, dbm.record_to_host_data)
        return records
    except Exception as e:
        logger.error(f"Error occurred in get_host_data_by_job_id: {e}")
        raise
    finally:
        connection.close()
        logger.info("Database connection closed.")


# ------------------------------- Functions for the job_data table -------------------------------


def get_job_data_by_id(job_data_id: str, row_limit: int = 100) -> list:
    """
    Retrieves job data records from the 'job_data' table filtered by the specified job data ID.

    This function establishes a database connection and executes a query to fetch records from the
    'job_data' table where the 'jid' column matches the provided job_data_id. The function limits
    the number of results to the specified row_limit. After fetching the records, they are converted
    into model instances using a designated conversion function. The function logs significant events
    and any errors encountered during its execution.

    :param job_data_id: The job data ID used to filter the records in the 'job_data' table.
    :param row_limit: The maximum number of records to return, defaults to 100 if not specified.
    :return: A list of job data model instances corresponding to the fetched records. Returns None
             if the database connection cannot be established.
    """
    logger.info(f"Fetching job data for job_data_id: {job_data_id} with row limit: {row_limit}")

    connection = dbm.get_database_connection()
    if connection is None:
        logger.error("Failed to establish database connection.")
        return None

    query = "SELECT * FROM job_data WHERE jid = %s LIMIT %s"
    params = (job_data_id, row_limit)

    try:
        records = dbm.execute_query(connection, query, params)
        logger.info(f"Successfully executed query. Number of records fetched: {len(records)}")

        # Assuming a function like 'record_to_job_data' exists to convert records to model instances
        records = dbm.convert_to_model(records, dbm.record_to_job_data)
        return records
    except Exception as e:
        logger.error(f"Error occurred in get_job_data_by_id: {e}")
        raise
    finally:
        connection.close()
        logger.info("Database connection closed.")


def get_job_data_by_user(user_id: str, row_limit: int = 100) -> list:
    """
    Retrieves job data records from the 'job_data' table filtered by the specified user ID.

    This function establishes a database connection and executes a query to fetch records from the
    'job_data' table where the 'username' column matches the provided user_id. The function limits
    the number of results to the specified row_limit. After fetching the records, they are converted
    into model instances using a designated conversion function. The function logs significant events
    and any errors encountered during its execution.

    :param user_id: The user identifier used to filter the records in the 'job_data' table.
    :param row_limit: The maximum number of records to return, defaults to 100 if not specified.
    :return: A list of job data model instances corresponding to the fetched records. Returns None
             if the database connection cannot be established.
    """
    logger.info(f"Fetching job data for user_id: {user_id} with row limit: {row_limit}")

    connection = dbm.get_database_connection()
    if connection is None:
        logger.error("Failed to establish database connection.")
        return None

    query = "SELECT * FROM job_data WHERE username = %s LIMIT %s"
    params = (user_id, row_limit)

    try:
        records = dbm.execute_query(connection, query, params)
        logger.info(f"Successfully executed query. Number of records fetched: {len(records)}")

        # Assuming a function like 'record_to_job_data' exists to convert records to model instances
        records = dbm.convert_to_model(records, dbm.record_to_job_data)
        return records
    except Exception as e:
        logger.error(f"Error occurred in get_job_data_by_user: {e}")
        raise
    finally:
        connection.close()
        logger.info("Database connection closed.")


def get_job_data_by_job_name(job_name: str, row_limit: int = 100) -> list:
    """
    Retrieves job data records from the 'job_data' table filtered by the specified job name.

    This function connects to the database and executes a query to fetch records from the 'job_data' table
    where the 'jobname' column matches the given job_name. The number of records returned is limited to the
    specified row_limit. After fetching the records, they are converted into model instances. Key events and
    errors are logged.

    :param job_name: The name of the job used to filter the records.
    :param row_limit: The maximum number of records to return. Defaults to 100 if not specified.
    :return: A list of job data model instances corresponding to the fetched records.
    """

    logger.info(f"Fetching job data for job name: {job_name} with row limit: {row_limit}")

    connection = dbm.get_database_connection()
    if connection is None:
        logger.error("Failed to establish database connection.")
        return None

    query = "SELECT * FROM job_data WHERE jobname = %s LIMIT %s"
    params = (job_name, row_limit)

    try:
        records = dbm.execute_query(connection, query, params)
        logger.info(f"Successfully executed query. Number of records fetched: {len(records)}")

        return dbm.convert_to_model(records, dbm.record_to_job_data)
    except Exception as e:
        logger.error(f"Error occurred in get_job_data_by_job_name: {e}")
        raise
    finally:
        connection.close()
        logger.info("Database connection closed.")


def get_job_data_by_host_id(host_id: str, row_limit: int = 100) -> list:
    """
    Retrieves job data records from the 'job_data' table filtered by the specified host ID.

    This function connects to the database and executes a query to fetch records from the 'job_data' table
    where the 'host_list' column includes the given host_id. The number of records returned is limited to the
    specified row_limit. After fetching the records, they are converted into model instances. Key events and
    errors are logged during the process.

    :param host_id: The host identifier used to filter the records in the 'job_data' table.
    :param row_limit: The maximum number of records to return. Defaults to 100 if not specified.
    :return: A list of job data model instances corresponding to the fetched records.
    """

    logger.info(f"Fetching job data for host ID: {host_id} with row limit: {row_limit}")

    connection = dbm.get_database_connection()
    if connection is None:
        logger.error("Failed to establish database connection.")
        return None

    query = "SELECT * FROM job_data WHERE %s = ANY(host_list) LIMIT %s"
    params = (host_id, row_limit)

    try:
        records = dbm.execute_query(connection, query, params)
        logger.info(f"Successfully executed query. Number of records fetched: {len(records)}")

        return dbm.convert_to_model(records, dbm.record_to_job_data)
    except Exception as e:
        logger.error(f"Error occurred in get_job_data_by_host_id: {e}")
        raise
    finally:
        connection.close()
        logger.info("Database connection closed.")


def get_job_data_by_account(account_id: str, row_limit: int = 100) -> list:
    """
    Retrieves job data records from the 'job_data' table filtered by the specified account ID.

    This function connects to the database and executes a query to fetch records from the 'job_data' table
    where the 'account' column matches the given account_id. The number of records returned is limited to the
    specified row_limit. After fetching the records, they are converted into model instances. Key events and
    errors are logged during the process.

    :param account_id: The account identifier used to filter the records in the 'job_data' table.
    :param row_limit: The maximum number of records to return. Defaults to 100 if not specified.
    :return: A list of job data model instances corresponding to the fetched records.
    """

    logger.info(f"Fetching job data for account ID: {account_id} with row limit: {row_limit}")

    connection = dbm.get_database_connection()
    if connection is None:
        logger.error("Failed to establish database connection.")
        return None

    query = "SELECT * FROM job_data WHERE account = %s LIMIT %s"
    params = (account_id, row_limit)

    try:
        records = dbm.execute_query(connection, query, params)
        logger.info(f"Successfully executed query. Number of records fetched: {len(records)}")

        return dbm.convert_to_model(records, dbm.record_to_job_data)
    except Exception as e:
        logger.error(f"Error occurred in get_job_data_by_account: {e}")
        raise
    finally:
        connection.close()
        logger.info("Database connection closed.")


def get_job_data_by_exit_code(exit_code: str, row_limit: int = 100) -> list:
    """
    Retrieves job data records from the 'job_data' table filtered by the specified exit code.

    This function connects to the database and executes a query to fetch records from the 'job_data' table
    where the 'exitcode' column matches the given exit_code. The number of records returned is limited to the
    specified row_limit. After fetching the records, they are converted into model instances. Key events and
    errors are logged during the process.

    :param exit_code: The exit code used to filter the records in the 'job_data' table.
    :param row_limit: The maximum number of records to return. Defaults to 100 if not specified.
    :return: A list of job data model instances corresponding to the fetched records.
    """

    logger.info(f"Fetching job data for exit code: {exit_code} with row limit: {row_limit}")

    connection = dbm.get_database_connection()
    if connection is None:
        logger.error("Failed to establish database connection.")
        return None

    query = "SELECT * FROM job_data WHERE exitcode = %s LIMIT %s"
    params = (exit_code, row_limit)

    try:
        records = dbm.execute_query(connection, query, params)
        logger.info(f"Successfully executed query. Number of records fetched: {len(records)}")

        return dbm.convert_to_model(records, dbm.record_to_job_data)
    except Exception as e:
        logger.error(f"Error occurred in get_job_data_by_exit_code: {e}")
        raise
    finally:
        connection.close()
        logger.info("Database connection closed.")

