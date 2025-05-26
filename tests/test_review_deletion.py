import pytest
from app.__init__ import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'test_secret_key'
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_reviews(mocker):
    # Mockear las funciones usadas en el controlador
    mock_get_all_reviews = mocker.patch('app.controllers.review_controller.get_all_reviews')
    mock_save_reviews = mocker.patch('app.controllers.review_controller.save_reviews')
    mock_add_review = mocker.patch('app.controllers.review_controller.add_review')
    return {
        'get_all_reviews': mock_get_all_reviews,
        'save_reviews': mock_save_reviews,
        'add_review': mock_add_review
    }

def test_delete_review_existing(client, mock_reviews):
    mock_reviews['get_all_reviews'].return_value = [
        {"review_id": 1, "student_id": 1, "tutor_id": 2, "comment": "Buen tutor!", "rating": 5},
        {"review_id": 2, "student_id": 2, "tutor_id": 2, "comment": "Bien.", "rating": 4},
    ]
    response = client.post('/delete-review/1', follow_redirects=True)
    assert response.status_code == 200
    assert "Reseña eliminada exitosamente." in response.get_data(as_text=True)
    mock_reviews['save_reviews'].assert_called_once()

def test_delete_review_non_existent(client, mock_reviews):
    mock_reviews['get_all_reviews'].return_value = [
        {"review_id": 1, "student_id": 1, "tutor_id": 2, "comment": "Buen tutor!", "rating": 5}
    ]

    response = client.post('/delete-review/999', follow_redirects=True)
    assert response.status_code == 200
    assert "No se encontró la reseña a eliminar." in response.get_data(as_text=True)


def test_comment_not_appearing_after_deletion(client, mocker):
    # Patch en el módulo donde está la función home() que maneja /comments
    mock_get_all_reviews = mocker.patch('app.controllers.review_controller.get_all_reviews')

    # Antes de la eliminación
    mock_get_all_reviews.return_value = [
        {"review_id": 1, "student_id": 1, "tutor_id": 2, "comment": "Buen tutor!", "rating": 5},
        {"review_id": 2, "student_id": 2, "tutor_id": 2, "comment": "Bien.", "rating": 4},
    ]

    response = client.post('/delete-review/1', follow_redirects=True)
    assert response.status_code == 200

    # Después de la eliminación
    mock_get_all_reviews.return_value = [
        {"review_id": 2, "student_id": 2, "tutor_id": 2, "comment": "Bien.", "rating": 4},
    ]

    response = client.get('/comments')
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert "Buen tutor!" not in data
    assert "Bien." in data
