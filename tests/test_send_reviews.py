# import sys
# import os
# import pytest

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
# from app.app import app

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     return app.test_client()

# def test_valid_review_sent(client):
#     response = client.post('/send-review', data={
#         'student_id': 'EstudianteTest',
#         'tutor_id': 'TutorTest',
#         'session_id': 'Sesion de Java',
#         'review_id': '55555',
#         'rating': '4',
#         'comment': 'Buen tutor.'
#     })
#     assert response.status_code == 302  # Redirecciona

# def test_out_of_bounds_rating_sent(client):
#     response = client.post('/send-review', data={
#         'student_id': 'EstudianteTest',
#         'tutor_id': 'TutorTest',
#         'session_id': 'Sesion de Java',
#         'review_id': '55555',
#         'rating': '6',
#         'comment': 'Calificacion fuera de los limites.'
#     })
#     assert response.status_code == 302

# def test_not_number_rating_sent(client):
#     response = client.post('/send-review', data={
#         'student_id': 'EstudianteTest',
#         'tutor_id': 'TutorTest',
#         'session_id': 'Sesion de Java',
#         'review_id': '55555',
#         'rating': 'hola',
#         'comment': 'La calificacion no es un numero.'
#     })
#     assert response.status_code == 302

# def test_empty_rating_sent(client):
#     response = client.post('/send-review', data={
#         'student_id': 'EstudianteTest',
#         'tutor_id': 'TutorTest',
#         'session_id': 'Sesion de Java',
#         'review_id': '55555',
#         'comment': 'Sin calificacion.'
#     })
#     assert response.status_code == 302

# def test_review_without_comment(client):
#     response = client.post('/send-review', data={
#         'student_id': 'EstudianteTest',
#         'tutor_id': 'TutorTest',
#         'session_id': 'Sesion de Java',
#         'review_id': '55555',
#         'rating': '5'
#     })
#     assert response.status_code == 302
