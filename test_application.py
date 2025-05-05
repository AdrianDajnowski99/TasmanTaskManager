import pytest
import unittest
#
from application import api_status
#
import application
from unittest.mock import patch, MagicMock

# @patch.multiple('application.db_conn',
#                 connect_to_db=MagicMock(),
#                 disconnect_db=MagicMock())
                

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
    def test_api_get_single_task(self, mock_get_task):
        mock_get_task.return_value = {
            'id': 505250144450153,
            'title': 'Test Task_5',
            'description': '[05-05-2025]  This is a test task',
            'status': 'ND'
        }

        response = self.client.get('/api/tasks/single/505250144450153')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'id': 505250144450153,
            'title': 'Test Task_5',
            'description': '[05-05-2025]  This is a test task',
            'status': 'ND'
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
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            'message': "Task added successfully"
        }) 

    @patch('application.api_edit_task')
    def test_api_edit_task(self, mock_api_edit_task):
        mock_api_edit_task.return_value = {
            'message': 'Task updated successfully'
        }
        response = self.client.put('api/tasks/2037809335687457', json={
            'title': 'Updated Task',
            'description': 'This is an updated test task',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message': 'Task updated successfully'
        })

    @patch('application.api_update_task')
    def test_api_update_task(self, mock_api_update_task):
        mock_api_update_task.return_value = {
            'message': 'Task status updated successfully'
        }
        response = self.client.put('/api/tasks/Updated Task', json={
            'status': 'Done'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message': 'Task status updated successfully'
        })
    @patch('application.api_delete_task')
    def test_api_delete_task(self, mock_api_delete_task):
        mock_api_delete_task.return_value = {
            'message': 'Task deleted successfully'
        }
        response = self.client.delete('/api/tasks/Updated Task')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message': 'Task deleted successfully'
        })


    if __name__ == '__main__':
        unittest.main()
