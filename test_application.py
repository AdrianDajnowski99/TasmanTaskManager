import pytest
import unittest
#
from application import api_status
#
import application
from unittest.mock import patch 

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.client = application.app.test_client()


    @patch('application.api_status')
    def test_api_status(self, mock_api_status):
        mock_api_status.return_value = {
            'status': "API is online"
        }
        response = self.client.get('/api/tasks/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'status': "API is online"
        })

    if __name__ == '__main__':
        unittest.main()
