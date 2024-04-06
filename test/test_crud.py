import unittest
from unittest.mock import patch, MagicMock
from crud import (
    get_host_data_by_host_id, get_host_data_by_job_id, get_job_data_by_id,
    get_job_data_by_user, get_job_data_by_job_name, get_job_data_by_host_id,
    get_job_data_by_account, get_job_data_by_exit_code
)


class TestCrud(unittest.TestCase):
    @patch('crud.dbm.get_database_connection')
    @patch('crud.dbm.execute_query')
    @patch('crud.dbm.convert_to_model')
    def test_get_host_data_by_host_id(self, mock_convert_to_model, mock_execute_query, mock_get_database_connection):
        mock_connection = MagicMock()
        mock_get_database_connection.return_value = mock_connection
        mock_records = [{'id': 1, 'host': 'example.com', 'data': 'some data'}]
        mock_execute_query.return_value = mock_records
        mock_model_instances = ['model instance']
        mock_convert_to_model.return_value = mock_model_instances

        host_id = 'example.com'
        row_limit = 10
        result = get_host_data_by_host_id(host_id, row_limit)

        self.assertEqual(result, mock_model_instances)
        mock_get_database_connection.assert_called_once()
        mock_execute_query.assert_called_once_with(mock_connection, "SELECT * FROM host_data WHERE host = %s LIMIT %s",
                                                   (host_id, row_limit))
        mock_convert_to_model.assert_called_once_with(mock_records, mock_convert_to_model.record_to_host_data)
        mock_connection.close.assert_called_once()

    @patch('crud.dbm.get_database_connection')
    @patch('crud.dbm.execute_query')
    @patch('crud.dbm.convert_to_model')
    def test_get_host_data_by_job_id(self, mock_convert_to_model, mock_execute_query, mock_get_database_connection):
        mock_connection = MagicMock()
        mock_get_database_connection.return_value = mock_connection
        mock_records = [{'id': 1, 'jid': 'job123', 'data': 'some data'}]
        mock_execute_query.return_value = mock_records
        mock_model_instances = ['model instance']
        mock_convert_to_model.return_value = mock_model_instances

        job_data_id = 'job123'
        row_limit = 10
        result = get_host_data_by_job_id(job_data_id, row_limit)

        self.assertEqual(result, mock_model_instances)
        mock_get_database_connection.assert_called_once()
        mock_execute_query.assert_called_once_with(mock_connection, "SELECT * FROM host_data WHERE jid = %s LIMIT %s",
                                                   (job_data_id, row_limit))
        mock_convert_to_model.assert_called_once_with(mock_records, mock_convert_to_model.record_to_host_data)
        mock_connection.close.assert_called_once()

    @patch('crud.dbm.get_database_connection')
    @patch('crud.dbm.execute_query')
    @patch('crud.dbm.convert_to_model')
    def test_get_job_data_by_id(self, mock_convert_to_model, mock_execute_query, mock_get_database_connection):
        mock_connection = MagicMock()
        mock_get_database_connection.return_value = mock_connection
        mock_records = [{'id': 1, 'jid': 'job123', 'data': 'some data'}]
        mock_execute_query.return_value = mock_records
        mock_model_instances = ['model instance']
        mock_convert_to_model.return_value = mock_model_instances

        job_data_id = 'job123'
        row_limit = 10
        result = get_job_data_by_id(job_data_id, row_limit)

        self.assertEqual(result, mock_model_instances)
        mock_get_database_connection.assert_called_once()
        mock_execute_query.assert_called_once_with(mock_connection, "SELECT * FROM job_data WHERE jid = %s LIMIT %s",
                                                   (job_data_id, row_limit))
        mock_convert_to_model.assert_called_once_with(mock_records, mock_convert_to_model.record_to_job_data)
        mock_connection.close.assert_called_once()

    @patch('crud.dbm.get_database_connection')
    @patch('crud.dbm.execute_query')
    @patch('crud.dbm.convert_to_model')
    def test_get_job_data_by_user(self, mock_convert_to_model, mock_execute_query, mock_get_database_connection):
        mock_connection = MagicMock()
        mock_get_database_connection.return_value = mock_connection
        mock_records = [{'id': 1, 'username': 'user123', 'data': 'some data'}]
        mock_execute_query.return_value = mock_records
        mock_model_instances = ['model instance']
        mock_convert_to_model.return_value = mock_model_instances

        user_id = 'user123'
        row_limit = 10
        result = get_job_data_by_user(user_id, row_limit)

        self.assertEqual(result, mock_model_instances)
        mock_get_database_connection.assert_called_once()
        mock_execute_query.assert_called_once_with(mock_connection, "SELECT * FROM job_data WHERE username = %s LIMIT %s",
                                                   (user_id, row_limit))
        mock_convert_to_model.assert_called_once_with(mock_records, mock_convert_to_model.record_to_job_data)
        mock_connection.close.assert_called_once()

    @patch('crud.dbm.get_database_connection')
    @patch('crud.dbm.execute_query')
    @patch('crud.dbm.convert_to_model')
    def test_get_job_data_by_job_name(self, mock_convert_to_model, mock_execute_query, mock_get_database_connection):
        mock_connection = MagicMock()
        mock_get_database_connection.return_value = mock_connection
        mock_records = [{'id': 1, 'jobname': 'job_name', 'data': 'some data'}]
        mock_execute_query.return_value = mock_records
        mock_model_instances = ['model instance']
        mock_convert_to_model.return_value = mock_model_instances

        job_name = 'job_name'
        row_limit = 10
        result = get_job_data_by_job_name(job_name, row_limit)

        self.assertEqual(result, mock_model_instances)
        mock_get_database_connection.assert_called_once()
        mock_execute_query.assert_called_once_with(mock_connection, "SELECT * FROM job_data WHERE jobname = %s LIMIT %s",
                                                   (job_name, row_limit))
        mock_convert_to_model.assert_called_once_with(mock_records, mock_convert_to_model.record_to_job_data)
        mock_connection.close.assert_called_once()

    @patch('crud.dbm.get_database_connection')
    @patch('crud.dbm.execute_query')
    @patch('crud.dbm.convert_to_model')
    def test_get_job_data_by_host_id(self, mock_convert_to_model, mock_execute_query, mock_get_database_connection):
        mock_connection = MagicMock()
        mock_get_database_connection.return_value = mock_connection
        mock_records = [{'id': 1, 'host_list': ['host123'], 'data': 'some data'}]
        mock_execute_query.return_value = mock_records
        mock_model_instances = ['model instance']
        mock_convert_to_model.return_value = mock_model_instances

        host_id = 'host123'
        row_limit = 10
        result = get_job_data_by_host_id(host_id, row_limit)

        self.assertEqual(result, mock_model_instances)
        mock_get_database_connection.assert_called_once()
        mock_execute_query.assert_called_once_with(mock_connection, "SELECT * FROM job_data WHERE %s = ANY(host_list) LIMIT %s",
                                                   (host_id, row_limit))
        mock_convert_to_model.assert_called_once_with(mock_records, mock_convert_to_model.record_to_job_data)
        mock_connection.close.assert_called_once()

    @patch('crud.dbm.get_database_connection')
    @patch('crud.dbm.execute_query')
    @patch('crud.dbm.convert_to_model')
    def test_get_job_data_by_account(self, mock_convert_to_model, mock_execute_query, mock_get_database_connection):
        mock_connection = MagicMock()
        mock_get_database_connection.return_value = mock_connection
        mock_records = [{'id': 1, 'account': 'account123', 'data': 'some data'}]
        mock_execute_query.return_value = mock_records
        mock_model_instances = ['model instance']
        mock_convert_to_model.return_value = mock_model_instances

        account_id = 'account123'
        row_limit = 10
        result = get_job_data_by_account(account_id, row_limit)

        self.assertEqual(result, mock_model_instances)
        mock_get_database_connection.assert_called_once()
        mock_execute_query.assert_called_once_with(mock_connection, "SELECT * FROM job_data WHERE account = %s LIMIT %s",
                                                   (account_id, row_limit))
        mock_convert_to_model.assert_called_once_with(mock_records, mock_convert_to_model.record_to_job_data)
        mock_connection.close.assert_called_once()

    @patch('crud.dbm.get_database_connection')
    @patch('crud.dbm.execute_query')
    @patch('crud.dbm.convert_to_model')
    def test_get_job_data_by_exit_code(self, mock_convert_to_model, mock_execute_query, mock_get_database_connection):
        mock_connection = MagicMock()
        mock_get_database_connection.return_value = mock_connection
        mock_records = [{'id': 1, 'exitcode': 0, 'data': 'some data'}]
        mock_execute_query.return_value = mock_records
        mock_model_instances = ['model instance']
        mock_convert_to_model.return_value = mock_model_instances

        exit_code = 0
        row_limit = 10
        result = get_job_data_by_exit_code(exit_code, row_limit)

        self.assertEqual(result, mock_model_instances)
        mock_get_database_connection.assert_called_once()
        mock_execute_query.assert_called_once_with(mock_connection, "SELECT * FROM job_data WHERE exitcode = %s LIMIT %s",
                                                   (exit_code, row_limit))
        mock_convert_to_model.assert_called_once_with(mock_records, mock_convert_to_model.record_to_job_data)
        mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()