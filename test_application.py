import unittest
from unittest import mock
import sys
import os
from unittest.mock import patch, MagicMock, ANY

# Mock database connection before importing application
with patch('psycopg2.connect') as mock_connect:
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Now import application after mocking the database connection
    import application

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.client = application.app.test_client()
        self.client.testing = True

        # Mock database connection for all tests
        self.db_patcher = patch('application.db_conn.connect_to_db')
        self.mock_db = self.db_patcher.start()
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_db.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor

    def tearDown(self):
        self.db_patcher.stop()

    def test_api_status(self):
        response = self.client.get('/api/tasks/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'API is online'})
    # ------------------------------------------------------------

    @patch('application.testing.get_single_task_by_id')
    def test_api_get_single_task(self, mock_get_task):
        mock_get_task.return_value = (
            515151515151515,
            'TestTask_Mock',
            'This is a test task',
            'ND'
        )

        response = self.client.get('/api/tasks/single/515151515151515')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'id': 515151515151515,
            'title': 'TestTask_Mock',
            'description': 'This is a test task',
            'status': 'ND'
        })
    # ------------------------------------------------------------

    @patch('application.controls.get_all_tasks')
    def test_api_get_all_tasks(self, mock_get_all_tasks):
        mock_get_all_tasks.return_value = [
            {'id': 515151515151515, 'title': 'Task1', 'description': 'Desc1', 'status': 'ND'},
            {'id': 525252525252525, 'title': 'Task2', 'description': 'Desc2', 'status': 'Done'}
        ]

        response = self.client.get('/api/tasks/all?sort_by=id&order=asc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)
        self.assertEqual(response.get_json()[0]['title'], 'Task1')
        
        mock_get_all_tasks.assert_called_once_with(ANY, 'id', 'asc')
    # ------------------------------------------------------------

    @patch('application.controls.add_task')
    def test_api_add_task(self, mock_add_task):
        mock_add_task.return_value = None
        
        response = self.client.post('/api/tasks/', json={
            'title': 'Test Task 0',
            'description': 'This is a test task',
            'status': 'ND'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'message': 'Task added successfully'})
        mock_add_task.assert_called_once()
    # ------------------------------------------------------------

    @patch('application.controls.get_all_existing_ids')
    @patch('application.testing.get_single_task_by_id')
    @patch('application.controls.edit_task')
    def test_api_edit_task(self, mock_edit_task, mock_get_task, mock_get_all_ids):
        mock_get_all_ids.return_value = [515151515151515]

        mock_get_task.return_value = (
            515151515151515, 
            'TestTask_Mock', 
            'This is a test task', 
            'ND'
        )
        new_title = "TestTask_Updated"
        new_description = "Updated task description"
        mock_edit_task.return_value = None 

        response = self.client.put('/api/tasks/515151515151515', json={
            'title': new_title,
            'description': new_description
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Task updated successfully'})

        mock_get_task.return_value = (
            515151515151515, 
            new_title,  
            new_description,  
            'ND')

        response = self.client.get('/api/tasks/single/515151515151515')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['title'], new_title)
        self.assertEqual(response.get_json()['description'], new_description)
    # ------------------------------------------------------------

    @patch('application.controls.get_all_existing_titles')
    @patch('application.testing.get_single_task_by_id')
    @patch('application.controls.update_task')
    def test_api_update_task(self, mock_update_task, mock_get_task, mock_get_all_titles):
        mock_get_all_titles.return_value = ['TestTask_Mock']
        
        mock_get_task.return_value = (
            515151515151515, 
            'TestTask_Mock', 
            'This is a test task', 
            'ND'
        )
        new_status = "Done"
        mock_update_task.return_value = None 

        response = self.client.put('/api/tasks/TestTask_Mock', json={
            'status': 'Done',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Task status updated successfully'})

        mock_get_task.return_value = (
            515151515151515, 
            'TestTask_Mock', 
            'This is a test task',
            new_status)

        response = self.client.get('/api/tasks/single/515151515151515')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], new_status)
    # ------------------------------------------------------------

    @patch('application.controls.get_all_existing_titles')
    @patch('application.testing.get_single_task_by_id')
    @patch('application.controls.delete_task')
    def test_api_delete_task(self, mock_delete_task, mock_get_task, mock_get_all_titles):
        mock_get_all_titles.return_value = ['TestTask_DeleteMe']
        
        mock_get_task.return_value = (
            515151515151515, 
            'TestTask_DeleteMe', 
            'Delete Me', 
            'In Progress'
        )
        mock_delete_task.return_value = None 
        response = self.client.delete('/api/tasks/TestTask_DeleteMe')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Task deleted successfully'})
        mock_delete_task.assert_called_once_with('TestTask_DeleteMe', mock.ANY)
    # ------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
