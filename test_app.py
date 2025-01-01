import unittest
from unittest.mock import patch, MagicMock
import jwt
from main import app, SECRET_KEY, ALGORITHM
import firebase_admin
from firebase_admin import firestore

class TestFavoritesAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # Test için token oluştur
        self.test_token = jwt.encode(
            {"sub": "test_user"},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        self.headers = {
            'Authorization': f'Bearer {self.test_token}',
            'Content-Type': 'application/json'
        }
        
        # Firestore mock
        self.firestore_mock = MagicMock()
        self.collection_mock = MagicMock()
        self.doc_mock = MagicMock()
        
        # Mock zinciri oluştur
        self.firestore_mock.collection.return_value = self.collection_mock
        self.collection_mock.document.return_value = self.doc_mock
        self.doc_mock.collection.return_value = self.collection_mock
        
        # where sorgusu için mock
        self.query_mock = MagicMock()
        self.collection_mock.where.return_value = self.query_mock
        self.query_mock.get.return_value = []

    @patch('firebase_admin.firestore.client')
    @patch('main.load_platform_data')
    def test_add_to_favorites(self, mock_load_data, mock_firestore):
        # Firestore mock'u ayarla
        mock_firestore.return_value = self.firestore_mock
        
        # Mock veri hazırla
        mock_load_data.return_value = [
            {
                'id': '1',
                'title': 'Test Game',
                'platform': 'steam',
                'price': '29.99'
            }
        ]
        
        response = self.app.post(
            '/api/favorites',
            json={'platform': 'steam'},
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    @patch('firebase_admin.firestore.client')
    @patch('main.load_platform_data')
    def test_no_data_found(self, mock_load_data, mock_firestore):
        # Firestore mock'u ayarla
        mock_firestore.return_value = self.firestore_mock
        
        # Boş veri döndür
        mock_load_data.return_value = []
        
        response = self.app.post(
            '/api/favorites',
            json={'platform': 'invalid_platform'},
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    @patch('firebase_admin.firestore.client')
    def test_missing_token(self, mock_firestore):
        # Firestore mock'u ayarla
        mock_firestore.return_value = self.firestore_mock
        
        response = self.app.post(
            '/api/favorites',
            json={'platform': 'steam'},
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json)

    @patch('firebase_admin.firestore.client')
    def test_invalid_token(self, mock_firestore):
        # Firestore mock'u ayarla
        mock_firestore.return_value = self.firestore_mock
        
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        
        response = self.app.post(
            '/api/favorites',
            json={'platform': 'steam'},
            headers=headers
        )
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()
