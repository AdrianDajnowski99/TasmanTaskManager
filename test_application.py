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

    @patch('application.api_get_single_task')
    def test_api_get_single_task(self, mock_api_get_single_task):
        mock_api_get_single_task.return_value = {
            'id': 2037809335687457,
        }
        response = self.client.get('/api/tasks/single/2037809335687457')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'id': 2037809335687457,

        })

    @patch('application.api_add_task')
    def test_api_add_task(self, mock_api_add_task):
        mock_api_add_task.return_value = {
            'message': "Task added successfully"
        }
        response = self.client.post('/api/tasks/', json={
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'ND'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message': "Task added successfully"
        }) 
        



    if __name__ == '__main__':
        unittest.main()
