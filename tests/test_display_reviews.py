import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from app.app import app

class TestReviewDisplay(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_page_exists(self):
        response = self.client.get('/')  # ID de tutor
        self.assertEqual(response.status_code, 200)

    def test_displays_new_reviews(self):
        self.client.post('/send-review', data={
            'student_id': 'EstudianteTest',
            'tutor_id': 'TutorTest',
            'session_id': '321',
            'rating': '3',
            'comment': 'Ni bueno ni malo.'
        })

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ni bueno ni malo.', response.data)

if __name__ == '__main__':
    unittest.main()