import pytest
from app.__init__ import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'test_secret_key' 
    with app.test_client() as client:
        yield client

def test_user_can_select_rating_from_1_to_5(client):
    for rating in range(1, 6):
        response = client.post('/send-review', data={
            'student_id': 'EstudianteTest',
            'tutor_id': 'TutorTest',
            'session_id': 'SesionTest',
            'review_id': str(10000 + rating),
            'rating': str(rating),
            'comment': f'Calificación de {rating} estrellas.'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert f'Calificación de {rating} estrellas.' in response.get_data(as_text=True)

def test_rating_appears_with_comment(client):
    response = client.post('/send-review', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'SesionTest',
        'review_id': '55557',
        'rating': '4',
        'comment': 'Comentario con calificación.'
    }, follow_redirects=True)

    assert response.status_code == 200

    response = client.get('/comments')
    data = response.get_data(as_text=True)
    assert 'Comentario con calificación.' in data
    assert '4' in data

def test_comment_without_rating_is_rejected(client):
    response = client.post('/send-review', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'SesionTest',
        'review_id': '55558',
        'rating': '',  # sin calificación
        'comment': 'Comentario sin calificación.'
    }, follow_redirects=True)

    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert 'La calificación no puede estar vacía' in data 
    assert 'Comentario sin calificación.' not in data
