import pytest
from app.__init__ import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'test_secret_key' 
    with app.test_client() as client:
        yield client

def test_valid_review_submission(client):
    response = client.post('/send-review', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'Sesion de Java',
        'review_id': '55555',
        'rating': '4',
        'comment': 'Buen tutor.'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Reseña enviada correctamente' in response.get_data(as_text=True)

def test_rating_above_maximum(client):
    response = client.post('/send-review', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'Sesion de Java',
        'review_id': '55556',
        'rating': '6',
        'comment': 'Muy bueno'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'La calificación debe estar entre 1 y 5.' in response.get_data(as_text=True)

def test_rating_not_a_number(client):
    response = client.post('/send-review', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'Sesion de Java',
        'review_id': '55557',
        'rating': 'abc',
        'comment': 'No es número'
    }, follow_redirects=True)
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert 'La calificación debe ser un número válido' in body or 'número entero válido' in body

def test_empty_rating(client):
    response = client.post('/send-review', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'Sesion de Java',
        'review_id': '55558',
        'comment': 'Falta rating'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'La calificación no puede estar vac' in response.get_data(as_text=True)

def test_empty_comment(client):
    response = client.post('/send-review', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'Sesion de Java',
        'review_id': '55559',
        'rating': '4',
        'comment': '   '
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'El comentario no puede estar vac' in response.get_data(as_text=True)
