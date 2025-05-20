# import sys
# import os
# import pytest

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
# from app.app import app

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     return app.test_client()

# def test_page_exists(client):
#     response = client.get('/comments')  # ID de tutor
#     assert response.status_code == 200

# def test_displays_new_reviews(client):
#     client.post('/send-review', data={
#         'student_id': 'EstudianteTest',
#         'tutor_id': 'TutorTest',
#         'session_id': 'Sesion de Java',
#         'review_id': '55555',
#         'rating': '3',
#         'comment': 'Ni bueno ni malo.'
#     })

#     response = client.get('/')
#     assert response.status_code == 200
#     assert b'Ni bueno ni malo.' in response.data
