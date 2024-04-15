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

    @patch('app.request')

    def test_insert_user_firebase(self, mock_request):
        mock_request.form = {'username': 'test', 'email': 'test@gmail.com', 'password': 'test', 'admin': False}
        response = self.app.post('/register')
        self.assertEqual(response.status_code, 200)

    def test_get_all_products(self):
        response = self.app.get('/all-products')
        self.assertEqual(response.status_code, 200)

    @patch('app.request')
    def test_insert_product(self, mock_request):
        mock_request.get_json = Mock(return_value={'name': 'test', 'specifications': 'test', 'description': 'test'})
        response = self.app.post('/insert-product')
        self.assertEqual(response.status_code, 200)

    def test_search_products(self):
        response = self.app.get('/search-products?query=test')
        self.assertEqual(response.status_code, 200)

    def test_get_picture_url(self):
        response = self.app.get('/get-picture-url')
        self.assertEqual(response.status_code, 200)

    @patch('your_flask_file.request')
    def test_upload_picture(self, mock_request):
        mock_request.get_json = Mock(return_value={'picture': base64.b64encode(b'test').decode()})
        with patch('builtins.open', new=mock_open()) as m:
            response = self.app.post('/upload-picture')
        self.assertEqual(response.status_code, 200)



    

if __name__ == '__main__':
    unittest.main()
