import inspect
import os
import psycopg2
import logging
import models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_database_connection():
    """
    Establishes a connection to the PostgreSQL database using psycopg2.

    This function attempts to establish a database connection using credentials
    retrieved from environment variables (DBHOST, DBPW, DBNAME, DBUSER). If any
    credential is missing or if the connection attempt fails, the function logs
    the error and returns None.

    :return: A psycopg2 database connection object if successful, None otherwise.
    """
    try:
        # Retrieve database credentials
        db_host = os.getenv('DBHOST')
        db_password = os.getenv('DBPW')
        db_name = os.getenv('DBNAME')
        db_user = os.getenv('DBUSER')

        # Log the presence of credentials
        credentials_status = {
            'DBHOST': 'present' if db_host else 'missing',
            'DBNAME': 'present' if db_name else 'missing',
            'DBUSER': 'present' if db_user else 'missing',
            'DBPW': 'present' if db_password else 'missing'
        }
        logger.info(f"Database credentials status: {credentials_status}")

        # Check all credentials are present
        if not all([db_host, db_password, db_name, db_user]):
            raise ValueError('One or more database credentials are missing.')

        # Attempt to establish a database connection
        connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        logger.info("Database connection established successfully.")
        return connection
    except Exception as error:
        logger.error(f"Database connection error: {error}")
        return None


def execute_query(connection, query, params=None):
    """
    Executes a SQL query on the given database connection.

    This function uses the provided database connection to execute a SQL query.
    It is designed to handle SELECT queries that return data. The function
    attempts to execute the given query and fetch all the results. If an error
    occurs during query execution, it logs the error and raises the exception.

    :param connection: The database connection object to use for executing the query.
    :param query: The SQL query string to be executed.
    :param params: Optional parameters to be passed with the query. Defaults to None.
    :return: A list of tuples containing the query results.
    """
    try:
        with connection.cursor() as cursor:
            # Log the start of the query execution
            logger.debug(f"Executing query: {query[:50]}...")  # Log only the first 50 characters of the query

            cursor.execute(query, params)

            # Fetch and return the results
            results = cursor.fetchall()
            logger.info(f"Query executed successfully. Number of records fetched: {len(results)}")
            return results
    except Exception as error:
        # Log the error without revealing sensitive query details
        logger.error(f"Error executing query: {error}")
        raise


def convert_to_model(data, conversion_function):
    """
    Convert query results (list of tuples) into model instances using a provided conversion function.

    :param data: List of tuples, each representing a database record.
    :param conversion_function: A function that takes a tuple and returns a model instance.
    :return: List of model instances.
    """
    try:
        logger.info("Starting conversion of query results to model instances.")
        converted_data = [conversion_function(record) for record in data]
        logger.info(f"Conversion successful. Number of records converted: {len(converted_data)}")
        return converted_data
    except Exception as error:
        logger.error(f"Error during conversion: {error}")
        raise


def record_to_host_data(record):
    """
    Converts a database record tuple into a HostData model instance.

    This function takes a tuple representing a single record from the 'host_data'
    table and maps its elements to the corresponding fields of the HostData model.
    The resulting object is an instance of the HostData model, ready for use in
    the application.

    :param record: A tuple containing the fields of a single 'host_data' record.
    :return: An instance of the HostData model populated with data from the record.
    """
    try:
        # model_fields = inspect.signature(models.HostData).parameters  # not working
        expected_length = 9

        if len(record) != expected_length:
            raise ValueError(f"Invalid record length. Expected {expected_length} elements.")

        host_data_instance = models.HostData(
            time=record[0], host=record[1], jid=record[2], type=record[3],
            event=record[4], unit=record[5], value=record[6], diff=record[7], arc=record[8]
        )
        logger.debug("Successfully converted database record to HostData model instance.")
        return host_data_instance
    except Exception as error:
        logger.error(f"Error in converting record to HostData model: {error}")
        raise


def record_to_job_data(record):
    """
    Converts a database record tuple into a JobData model instance.

    This function takes a tuple representing a single record from the 'job_data'
    table and maps its elements to the corresponding fields of the JobData model.
    The resulting object is an instance of the JobData model, encapsulating all
    the job-related data in a structured format, suitable for use throughout the
    application.

    :param record: A tuple containing the fields of a single 'job_data' record.
    :return: An instance of the JobData model populated with data from the record.
    """
    try:
        # model_fields = inspect.signature(models.HostData).parameters  # not working
        expected_length = 17

        if len(record) != expected_length:
            raise ValueError(f"Invalid record length. Expected {expected_length} elements.")

        job_data_instance = models.JobData(
            jid=record[0],
            submit_time=record[1],
            start_time=record[2],
            end_time=record[3],
            runtime=record[4],
            timelimit=record[5],
            node_hrs=record[6],
            nhosts=record[7],
            ncores=record[8],
            ngpus=record[9],
            username=record[10],
            account=record[11],
            queue=record[12],
            state=record[13],
            jobname=record[14],
            exitcode=record[15],
            host_list=record[16]
        )
        logger.debug("Successfully converted database record to JobData model instance.")
        return job_data_instance
    except Exception as error:
        logger.error(f"Error in converting record to JobData model: {error}")
        raise
