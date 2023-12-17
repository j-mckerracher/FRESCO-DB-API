import pytest
from datetime import datetime
import main
import schemas
from unittest import mock
from fastapi import HTTPException


@pytest.fixture(autouse=True)
def mock_dependencies():
    with mock.patch('main.get_db_and_user', return_value=(mock.Mock(), mock.Mock())):
        yield


@pytest.fixture
def mock_db():
    return mock.Mock()


@pytest.fixture
def mock_user():
    return mock.Mock()


# Fixture for mock data
@pytest.fixture
def mock_data_2():
    return [schemas.JobData(
        jid=str(i),
        submit_time=datetime.now(),
        start_time=datetime.now(),
        end_time=datetime.now(),
        runtime=123.0,
        timelimit=123.0,
        node_hrs=123.0,
        nhosts=123,
        ncores=123,
        ngpus=123,
        username=f'test_user_{i}',
        account='test_account',
        queue='test_queue',
        state='test_state',
        jobname=f'Job {i}',
        exitcode='0',
        host_list=['host1', 'host2']
    ) for i in range(2)]


# Fixture for mock data
@pytest.fixture
def mock_data_301():
    return [schemas.JobData(
        jid=str(i),
        submit_time=datetime.now(),
        start_time=datetime.now(),
        end_time=datetime.now(),
        runtime=123.0,
        timelimit=123.0,
        node_hrs=123.0,
        nhosts=123,
        ncores=123,
        ngpus=123,
        username=f'test_user_{i}',
        account='test_account',
        queue='test_queue',
        state='test_state',
        jobname=f'Job {i}',
        exitcode='0',
        host_list=['host1', 'host2']
    ) for i in range(301)]


class TestReadJobDataSingleJid:

    @mock.patch('main.crud.get_job_data_by_id')
    def test_returns_list_of_job_data_records(self, mock_get_job_data_by_id, mock_db, mock_user, mock_data_2):
        job_id = "valid_job_id"
        mock_get_job_data_by_id.return_value = mock_data_2
        result = main.read_job_data_single_jid(job_id, (mock_db, mock_user))
        assert result == mock_data_2

    @mock.patch('main.crud.get_job_data_by_id', return_value=[])
    def test_raises_http_exception_when_no_records_found(self, _):
        job_id = "invalid_job_id"
        with pytest.raises(HTTPException) as e:
            main.read_job_data_single_jid(job_id, (mock_db, mock_user))
        assert e.value.status_code == 500

    @mock.patch('main.crud.get_job_data_by_id', side_effect=Exception("Database error"))
    def test_raises_http_exception_when_error_fetching_records(self, _):
        job_id = "valid_job_id"
        with pytest.raises(HTTPException) as e:
            main.read_job_data_single_jid(job_id, (mock_db, mock_user))
        assert e.value.status_code == 500

    @mock.patch('main.crud.get_job_data_by_id')
    def test_returns_list_of_job_data_records_when_more_than_300_records(self, mock_get_job_data_by_id):
        mock_data = mock_data_301  # Simulate 301 records
        mock_get_job_data_by_id.return_value = mock_data

        job_id = "valid_job_id"
        result = main.read_job_data_single_jid(job_id, (mock_db, mock_user))
        assert result == mock_data

    @mock.patch('main.crud.get_job_data_by_id', side_effect=Exception("Error closing database session"))
    def test_raises_http_exception_when_error_closing_database_session(self, _):
        job_id = "valid_job_id"
        with pytest.raises(HTTPException) as e:
            main.read_job_data_single_jid(job_id, (mock_db, mock_user))
        assert e.value.status_code == 500

    # **************************************************************************
    # !!!!!!!!!! ----------- JOB DATA SINGLE USER ----------- !!!!!!!!!! #######
    # **************************************************************************

    @mock.patch('main.crud.get_job_data_by_user')
    def test_successful_job_data_retrieval(self, mock_get_job_data_by_user, mock_db, mock_user):
        # Arrange
        user_id = "test_user_id"
        mock_data = mock_data_2
        mock_get_job_data_by_user.return_value = mock_data

        # Act
        result = main.read_job_data_single_user(user_id, (mock_db, mock_user))

        # Assert
        assert result == mock_data

    @mock.patch('main.crud.get_job_data_by_user', return_value=[])
    def test_no_records_found(self, mock_get_job_data_by_user, mock_db, mock_user):
        # Arrange
        user_id = "non_existing_user"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            main.read_job_data_single_user(user_id, (mock_db, mock_user))
        assert exc_info.value.status_code == 500

    @mock.patch('main.crud.get_job_data_by_user', side_effect=Exception("Database error"))
    def test_database_error(self, mock_get_job_data_by_user, mock_db, mock_user):
        # Arrange
        user_id = "valid_user_id"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            main.read_job_data_single_user(user_id, (mock_db, mock_user))
        assert exc_info.value.status_code == 500

    # **************************************************************************
    # !!!!!!!!!! ----------- JOB DATA SINGLE JOB NAME ----------- !!!!!!!!!! ###
    # **************************************************************************

    @mock.patch('main.crud.get_job_data_by_job_name')
    def test_returns_list_of_job_data_records_jn(self, mock_get_job_data_by_job_name, mock_db, mock_user, mock_data_2):
        job_id = "valid_job_id"
        mock_get_job_data_by_job_name.return_value = mock_data_2
        result = main.read_job_data_single_job_name(job_id, (mock_db, mock_user))
        assert result == mock_data_2

    @mock.patch('main.crud.get_job_data_by_job_name', return_value=[])
    def test_raises_http_exception_when_no_records_found_jn(self, _):
        job_id = "invalid_job_id"
        with pytest.raises(HTTPException) as e:
            main.read_job_data_single_job_name(job_id, (mock_db, mock_user))
        assert e.value.status_code == 500

    @mock.patch('main.crud.get_job_data_by_job_name', side_effect=Exception("Database error"))
    def test_raises_http_exception_when_error_fetching_records_jn(self, _):
        job_id = "valid_job_id"
        with pytest.raises(HTTPException) as e:
            main.read_job_data_single_job_name(job_id, (mock_db, mock_user))
        assert e.value.status_code == 500

    @mock.patch('main.crud.get_job_data_by_job_name')
    def test_returns_list_of_job_data_records_when_more_than_300_records_jn(self, mock_get_job_data_by_job_name):
        mock_data = mock_data_301  # Simulate 301 records
        mock_get_job_data_by_job_name.return_value = mock_data

        job_id = "valid_job_id"
        result = main.read_job_data_single_job_name(job_id, (mock_db, mock_user))
        assert result == mock_data

    @mock.patch('main.crud.get_job_data_by_job_name', side_effect=Exception("Error closing database session"))
    def test_raises_http_exception_when_error_closing_database_session_jn(self, _):
        job_id = "valid_job_id"
        with pytest.raises(HTTPException) as e:
            main.read_job_data_single_job_name(job_id, (mock_db, mock_user))
        assert e.value.status_code == 500
