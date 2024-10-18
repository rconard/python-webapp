import unittest
import json
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test."""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        """Test the home route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Assuming the home route returns the index.html file
        self.assertIn(b'<!doctype html>', response.data)

    def test_echo_api_with_valid_json(self):
        """Test the echo API with valid JSON data."""
        test_data = {"message": "Hello, World!"}
        response = self.app.post('/api/echo',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, test_data)

    def test_echo_api_with_invalid_json(self):
        """Test the echo API with invalid JSON data."""
        response = self.app.post('/api/echo',
                                 data='This is not JSON',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 415)

    def test_echo_api_with_empty_request(self):
        """Test the echo API with an empty request."""
        response = self.app.post('/api/echo',
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

    def test_echo_api_missing_content_type(self):
        """Test the echo API with missing Content-Type header."""
        test_data = {"message": "Hello, World!"}
        response = self.app.post('/api/echo',
                                 data=json.dumps(test_data))
        self.assertEqual(response.status_code, 415)

    def test_echo_api_non_json_content_type(self):
        """Test the echo API with non-JSON content type."""
        response = self.app.post('/api/echo',
                                 data='This is not JSON',
                                 content_type='text/plain')
        self.assertEqual(response.status_code, 415)

    def test_echo_special_characters(self):
        """Test the echo API with special characters."""
        response = self.app.post('/api/echo',
                                 data=json.dumps({"message": "!@#$%^&*()"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "!@#$%^&*()"})

    def test_echo_long_message(self):
        """Test the echo API with a long message."""
        long_message = 'a' * 1000
        response = self.app.post('/api/echo',
                                 data=json.dumps({"message": long_message}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": long_message})


    def test_echo_api_missing_content_type(self):
        """Test the echo API with missing Content-Type header."""
        test_data = {"message": "Hello, World!"}
        response = self.app.post('/api/echo',
                                 data=json.dumps(test_data))
        self.assertEqual(response.status_code, 415)

    def test_echo_api_non_json_content_type(self):
        """Test the echo API with non-JSON content type."""
        response = self.app.post('/api/echo',
                                 data='This is not JSON',
                                 content_type='text/plain')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
    
