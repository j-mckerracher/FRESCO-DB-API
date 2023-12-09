import unittest
from unittest.mock import MagicMock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
import main
from main import models


class UnitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mocked_session = UnifiedAlchemyMagicMock()

        self.mock_api_user = models.ApiUser(id=1, username='testuser', password_hash='hash')

        # Return a list of main.schemas.HostData objects instead of models.HostData
        self.host_data_mock_return = MagicMock(return_value=[
            main.schemas.HostData(
                time="2023-01-01 00:00:00",
                host="host1",
                jid="jid1",
                type="type1",
                event="event1",
                unit="unit1",
                value=1.0,
                diff=0.1,
                arc=0.2
            )
        ])

        self.expected_result_host_data_happy_path = self.host_data_mock_return.return_value

        main.crud.get_host_data_by_host_id = self.host_data_mock_return

    def test_read_host_data_single_node_happy_path(self):
        node_id = 'node123'
        # Mock the db_user tuple with the mocked session and an ApiUser instance
        db_user = (self.mocked_session, self.mock_api_user)

        # Call your function with the mocked session and node_id
        result = main.read_host_data_single_node(node_id, db_user=db_user)

        # Check if the result is as expected
        self.assertEqual(result, self.expected_result_host_data_happy_path)

    def test_read_host_data_single_node_no_data_found(self):
        node_id = 'node123'
        db_user = (self.mocked_session, self.mock_api_user)

        # Mock the get_host_data_by_host_id function to return an empty list
        main.crud.get_host_data_by_host_id.return_value = []

        with self.assertRaises(main.HTTPException) as context:
            main.read_host_data_single_node(node_id, db_user=db_user)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, f"Host data for node {node_id} not found")

    def test_read_host_data_single_node_unexpected_error(self):
        node_id = 'node123'
        db_user = (self.mocked_session, self.mock_api_user)

        # Mock the get_host_data_by_host_id function to raise an exception
        main.crud.get_host_data_by_host_id.side_effect = Exception("Database error")

        with self.assertRaises(main.HTTPException) as context:
            main.read_host_data_single_node(node_id, db_user=db_user)

        self.assertEqual(context.exception.status_code, 500)
        self.assertIn("Database error", context.exception.detail)


if __name__ == '__main__':
    unittest.main()
