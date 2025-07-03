import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, session
from app.controllers.tutorial_controller import unsubscribe_tutorial

class TestUnsubscribeController(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test_secret'
        self.app.add_url_rule('/tutorial/<id>/unsubscribe', 
                             view_func=unsubscribe_tutorial, 
                             methods=['POST'])
        
        self.client = self.app.test_client()
        
    @patch('app.controllers.tutorial_controller.firebase_repo')
    def test_unsubscribe_success(self, mock_repo):
        # Configurar mocks
        mock_repo.unregister_from_tutoria.return_value = True
        
        # Simular sesión de usuario
        with self.client.session_transaction() as sess:
            sess['user_id'] = 'student123'
            sess['role'] = 'Student'
        
        # Ejecutar
        response = self.client.post('/tutorial/tutoria123/unsubscribe')
        
        # Verificar
        mock_repo.unregister_from_tutoria.assert_called_with('student123', 'tutoria123')
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertIn('/subscriptions', response.location)
        
        # Verificar mensaje flash
        with self.client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            self.assertTrue(any('Te has desinscrito exitosamente' in msg for cat, msg in flashes))

    @patch('app.controllers.tutorial_controller.firebase_repo')
    def test_unsubscribe_failure(self, mock_repo):
        # Configurar mocks
        mock_repo.unregister_from_tutoria.return_value = False
        
        # Simular sesión de usuario
        with self.client.session_transaction() as sess:
            sess['user_id'] = 'student123'
            sess['role'] = 'Student'
        
        # Ejecutar
        response = self.client.post('/tutorial/tutoria123/unsubscribe')
        
        # Verificar
        mock_repo.unregister_from_tutoria.assert_called_with('student123', 'tutoria123')
        
        # Verificar mensaje flash
        with self.client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            self.assertTrue(any('No fue posible desinscribirte' in msg for cat, msg in flashes))

    @patch('app.controllers.tutorial_controller.firebase_repo')
    def test_unsubscribe_unauthenticated(self, mock_repo):
        # Sin sesión de usuario
        response = self.client.post('/tutorial/tutoria123/unsubscribe')
        
        # Verificar
        mock_repo.unregister_from_tutoria.assert_not_called()
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertIn('/auth/login', response.location)
        
        # Verificar mensaje flash
        with self.client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            self.assertTrue(any('Debe iniciar sesión' in msg for cat, msg in flashes))

    @patch('app.controllers.tutorial_controller.firebase_repo')
    def test_unsubscribe_wrong_role(self, mock_repo):
        # Usuario con rol incorrecto
        with self.client.session_transaction() as sess:
            sess['user_id'] = 'tutor123'
            sess['role'] = 'Tutor'  # No es Student
        
        response = self.client.post('/tutorial/tutoria123/unsubscribe')
        
        # Verificar
        mock_repo.unregister_from_tutoria.assert_not_called()
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertIn('/home', response.location)

if __name__ == '__main__':
    unittest.main()