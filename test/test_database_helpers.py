import unittest
from unittest.mock import patch, MagicMock
import database_helpers as dbm
import models


class TestDatabaseHelpers(unittest.TestCase):
    @patch.dict('os.environ', {'DBHOST': 'localhost', 'DBPW': 'password', 'DBNAME': 'testdb', 'DBUSER': 'testuser'})
    @patch('psycopg2.connect')
    def test_get_database_connection_success(self, mock_connect):
        dbm.get_database_connection()
        mock_connect.assert_called_once_with(host='localhost', dbname='testdb', user='testuser', password='password')

    @patch.dict('os.environ', {})
    def test_get_database_connection_missing_credentials(self):
        self.assertIsNone(dbm.get_database_connection())

    @patch('database_helpers.logger.debug')
    @patch('database_helpers.logger.info')
    def test_execute_query_success(self, mock_info, mock_debug):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('result1',), ('result2',)]

        results = dbm.execute_query(mock_connection, "SELECT * FROM test")

        mock_debug.assert_called_once_with("Executing query: SELECT * FROM test...")
        mock_cursor.execute.assert_called_once_with("SELECT * FROM test", None)
        mock_info.assert_called_once_with("Query executed successfully. Number of records fetched: 2")
        self.assertEqual(results, [('result1',), ('result2',)])

    @patch('database_helpers.logger.info')
    def test_convert_to_model_success(self, mock_info):
        mock_conversion_function = MagicMock(side_effect=lambda x: x)
        data = [('record1',), ('record2',)]

        converted_data = dbm.convert_to_model(data, mock_conversion_function)

        mock_info.assert_any_call("Starting conversion of query results to model instances.")
        mock_info.assert_called_with("Conversion successful. Number of records converted: 2")
        self.assertEqual(converted_data, [('record1',), ('record2',)])

    def test_record_to_host_data_success(self):
        record = (1, 'host1', 'jid1', 'type1', 'event1', 'unit1', 'value1', 'diff1', 'arc1')
        host_data = dbm.record_to_host_data(record)

        self.assertIsInstance(host_data, models.HostData)
        self.assertEqual(host_data.time, 1)
        self.assertEqual(host_data.host, 'host1')
        self.assertEqual(host_data.jid, 'jid1')
        self.assertEqual(host_data.type, 'type1')
        self.assertEqual(host_data.event, 'event1')
        self.assertEqual(host_data.unit, 'unit1')
        self.assertEqual(host_data.value, 'value1')
        self.assertEqual(host_data.diff, 'diff1')
        self.assertEqual(host_data.arc, 'arc1')

    def test_record_to_host_data_invalid_record_length(self):
        record = (1, 'host1', 'jid1', 'type1', 'event1', 'unit1', 'value1', 'diff1')
        with self.assertRaises(ValueError):
            dbm.record_to_host_data(record)

    def test_record_to_job_data_success(self):
        record = ('jid1', 1, 2, 3, 4, 5, 6, 7, 8, 9, 'user1', 'account1', 'queue1', 'state1', 'jobname1', 0, ['host1', 'host2'])
        job_data = dbm.record_to_job_data(record)

        self.assertIsInstance(job_data, models.JobData)
        self.assertEqual(job_data.jid, 'jid1')
        self.assertEqual(job_data.submit_time, 1)
        self.assertEqual(job_data.start_time, 2)
        self.assertEqual(job_data.end_time, 3)
        self.assertEqual(job_data.runtime, 4)
        self.assertEqual(job_data.timelimit, 5)
        self.assertEqual(job_data.node_hrs, 6)
        self.assertEqual(job_data.nhosts, 7)
        self.assertEqual(job_data.ncores, 8)
        self.assertEqual(job_data.ngpus, 9)
        self.assertEqual(job_data.username, 'user1')
        self.assertEqual(job_data.account, 'account1')
        self.assertEqual(job_data.queue, 'queue1')
        self.assertEqual(job_data.state, 'state1')
        self.assertEqual(job_data.jobname, 'jobname1')
        self.assertEqual(job_data.exitcode, 0)
        self.assertEqual(job_data.host_list, ['host1', 'host2'])

    def test_record_to_job_data_invalid_record_length(self):
        record = ('jid1', 1, 2, 3, 4, 5, 6, 7, 8, 9, 'user1', 'account1', 'queue1', 'state1', 'jobname1', 0)
        with self.assertRaises(ValueError):
            dbm.record_to_job_data(record)


if __name__ == '__main__':
    unittest.main()