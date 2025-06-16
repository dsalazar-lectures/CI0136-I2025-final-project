import pytest
from app.__init__ import app
import json
from pathlib import Path

# Ruta al archivo de reviews
JSON_PATH = Path(__file__).parent.parent / "app" / "models" / "reviews_data.json"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

import pytest
from app.__init__ import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'test_secret_key'
    with app.test_client() as client:
        yield client

def reset_reviews_data():
    """Restablece el archivo JSON con datos por defecto antes de cada prueba"""
    default_reviews = [
        {
            'student_id': 'Estudiante1',
            'rating': 5,
            'date': '05/04/2023',
            'comment': 'Excelente tutor.',
            'session_id': 'Sesion de Python',
            'review_id': 12345,
            'reply': None
        }
    ]
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(default_reviews, f, indent=2, ensure_ascii=False)

def test_add_valid_reply(client):
    reset_reviews_data()
    response = client.post('/reply-review/12345', data={
        'tutor_id': 'TutorTest',
        'comment': 'Gracias por tu comentario!'
    })
    assert response.status_code == 302

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
        review = next((r for r in reviews if r['review_id'] == 12345), None)
        assert review is not None
        assert 'replies' in review
        assert any(reply['comment'] == 'Gracias por tu comentario!' for reply in review['replies'])

def test_add_empty_reply_comment(client):
    reset_reviews_data()
    response = client.post('/reply-review/12345', data={
        'tutor_id': 'TutorTest',
        'comment': '    '
    })
    assert response.status_code == 302

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
        review = next((r for r in reviews if r['review_id'] == 12345), None)
        assert review is not None
        assert 'replies' not in review or len(review['replies']) == 0
