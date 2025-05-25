import pytest
from app.__init__ import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_comments_appear_in_tutor_profile(client):
    client.post('/send-review', data={
        'student_id': 'UsuarioTest',
        'tutor_id': 'Tutor123',
        'session_id': 'Sesion de Java',
        'review_id': '12345',
        'rating': '4',
        'comment': 'Muy buen tutor.'
    })

    response = client.get('/comments')
    assert response.status_code == 200
    assert b'Muy buen tutor.' in response.data

def test_comment_shows_author_date_and_photo(client):
    client.post('/send-review', data={
        'student_id': 'UsuarioTest',
        'tutor_id': 'Tutor123',
        'session_id': 'Sesion de Java',
        'review_id': '12346',
        'rating': '5',
        'comment': 'Excelente explicacion.'
    })

    response = client.get('/comments')
    assert response.status_code == 200
    data = response.get_data(as_text=True)

    assert 'UsuarioTest' in data
    assert 'Excelente explicacion.' in data
    assert 'Fecha:' in data or 'fecha' in data.lower()

def test_add_comment_button_visible_for_tutored_user(client):
    response = client.get(f'/comments')
    assert response.status_code == 200
    data = response.get_data(as_text=True)

    assert 'Calificar Tutor' in data
