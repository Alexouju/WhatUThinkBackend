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



if __name__ == '__main__':
    unittest.main()
