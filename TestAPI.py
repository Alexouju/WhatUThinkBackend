import base64
import unittest
from unittest.mock import patch, Mock, mock_open
from app import app, db, User
from firebase_admin import firestore

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.test_request_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.request')

    def test_login_firebase(self, mock_request):
        mock_request.form = {'username_or_email': 'test', 'password': 'test'}
        response = self.app.post('/login')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
