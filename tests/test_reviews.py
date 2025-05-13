import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from app.app import app

class TestReviewSent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_valid_review_sent(self):
        response = self.client.post('/send-review', data={
            'student_id': 'EstudianteTest',
            'tutor_id': 'TutorTest',
            'session_id': '123',
            'rating': '4',
            'comment': 'Buen tutor.'
        })
        self.assertEqual(response.status_code, 302)  # Redirecciona

    def test_out_of_bounds_rating_sent(self):
        response = self.client.post('/send-review', data={
            'student_id': 'EstudianteTest',
            'tutor_id': 'TutorTest',
            'session_id': '123',
            'rating': '6',
            'comment': 'Calificacion fuera de los limites.'
        })
        self.assertEqual(response.status_code, 400)  # Debe devolver error

    def test_not_number_rating_sent(self):
        response = self.client.post('/send-review', data={
            'student_id': 'EstudianteTest',
            'tutor_id': 'TutorTest',
            'session_id': '123',
            'rating': 'hola',
            'comment': 'La calificacion no es un numero.'
        })
        self.assertEqual(response.status_code, 400)  # Debe devolver error

    def test_empty_rating_sent(self):
        response = self.client.post('/send-review', data={
            'student_id': 'EstudianteTest',
            'tutor_id': 'TutorTest',
            'session_id': '123',
            'comment': 'Sin calificacion.'
        })
        self.assertEqual(response.status_code, 400)  # Debe devolver error

    def test_review_without_comment(self):
        response = self.client.post('/send-review', data={
            'student_id': 'EstudianteTest',
            'tutor_id': 'TutorTest',
            'session_id': '123',
            'rating': '5'
        })
        self.assertEqual(response.status_code, 302)  # Redirecciona

if __name__ == '__main__':
    unittest.main()