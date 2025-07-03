import pytest
from app.routes.review_routes import calculate_average_reviews
from unittest.mock import patch, MagicMock

@pytest.mark.parametrize("num_reviews,should_flash", [
    (5, True),   # menos de 10 -> muestra aviso
    (10, False), # 10 o más -> no muestra aviso
])
@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseTutoringRepository.get_tutorial_by_id')
@patch('app.routes.review_routes.FirebaseUserRepository.get_user_by_name')
def test_comments_render_average_and_flash(mock_get_user, mock_get_tutoria, mock_get_all_reviews, client, num_reviews, should_flash):
    # Preparar mocks
    mock_get_tutoria.return_value = MagicMock(tutor='Tutor1', title='Sesion1')
    mock_get_user.return_value = {'profile_picture_url': 'http://url.to/avatar.png'}
    
    # Crear reviews ficticios con rating 5, cantidad num_reviews
    mock_get_all_reviews.return_value = [
        {'session_id': 'Sesion1', 'rating': 5, 'student_id': f'student{i}', 'comment': 'Muy bien', 'review_id': i}  # <-- solo i, entero
        for i in range(num_reviews)
    ]

    response = client.get('/comments/some_tutoria_id')
    html = response.get_data(as_text=True)

    assert response.status_code == 200

    # Verificar promedio correcto en HTML
    expected_average = 5.0
    assert str(expected_average) in html

    # Verificar cantidad en HTML
    assert f"({num_reviews})" in html

    # Verificar que mensaje flash aparezca o no
    if should_flash:
        assert "Pocas calificaciones disponibles" in html
    else:
        assert "Pocas calificaciones disponibles" not in html

def test_calculate_average_reviews_empty():
    assert calculate_average_reviews([]) == 0.0

def test_calculate_average_reviews_correct_average():
    reviews = [{'rating': 5}, {'rating': 3}, {'rating': 4}]
    assert calculate_average_reviews(reviews) == 4.0

def test_calculate_average_reviews_rounding():
    reviews = [{'rating': 3}, {'rating': 4}]
    assert calculate_average_reviews(reviews) == 3.5