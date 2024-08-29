import unittest
from app import create_app
from app.routes import save_data, load_data

class FlaskCrudTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
        
        # Reset the data file for testing
        save_data([])

    def test_create_item(self):
        response = self.client.post('/api/items', json={'name': 'Test Item', 'value': 10})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Test Item')
        self.assertEqual(response.json['value'], 10)

    def test_get_items(self):
        self.client.post('/api/items', json={'name': 'Test Item', 'value': 10})
        response = self.client.get('/api/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_update_item(self):
        self.client.post('/api/items', json={'name': 'Test Item', 'value': 10})
        response = self.client.put('/api/items/1', json={'name': 'Updated Item', 'value': 20})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Item')
        self.assertEqual(response.json['value'], 20)

    def test_delete_item(self):
        self.client.post('/api/items', json={'name': 'Test Item', 'value': 10})
        response = self.client.delete('/api/items/1')
        self.assertEqual(response.status_code, 204)  # Check for status code only

    def tearDown(self):
        # Clean up after each test
        save_data([])

if __name__ == '__main__':
    unittest.main()