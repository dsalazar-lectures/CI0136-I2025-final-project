# import pytest
# from unittest.mock import MagicMock
# from flask import Flask
# from app.controllers.review_controller import delete_review, send_review
# from app.models.review_model import add_review, get_all_reviews, save_reviews

# @pytest.fixture
# def app():
#     app = Flask(__name__)
#     app.config['TESTING'] = True
#     return app

# @pytest.fixture
# def mock_reviews(mocker):
#     # Mock de las funciones de reviews
#     mock_get_all_reviews = mocker.patch('app.controllers.review_controller.get_all_reviews')
#     mock_save_reviews = mocker.patch('app.controllers.review_controller.save_reviews')
#     mock_add_review = mocker.patch('app.controllers.review_controller.add_review')
    
#     return {
#         'get_all_reviews': mock_get_all_reviews,
#         'save_reviews': mock_save_reviews,
#         'add_review': mock_add_review
#     }

# # Test para eliminar un comentario existente
# def test_delete_review_existing(mock_reviews, app):
#     mock_reviews['get_all_reviews'].return_value = [
#         {"review_id": 1, "student_id": 1, "tutor_id": 2, "comment": "Great tutor!", "rating": 5},
#         {"review_id": 2, "student_id": 2, "tutor_id": 2, "comment": "Good explanation.", "rating": 4},
#     ]
    
#     # Simula la eliminación de la reseña
#     review_id_to_delete = 1
#     with app.test_request_context():
#         result = delete_review(review_id_to_delete)

#     mock_reviews['save_reviews'].assert_called_once()
    
#     assert "Reseña eliminada exitosamente." in result.response.get_data(as_text=True)

# # Test para eliminar un comentario no existente
# def test_delete_review_non_existent(mock_reviews, app):
#     mock_reviews['get_all_reviews'].return_value = [
#         {"review_id": 1, "student_id": 1, "tutor_id": 2, "comment": "Great tutor!", "rating": 5}
#     ]
    
#     # Intentamos eliminar un comentario que no existe
#     review_id_to_delete = 999  # Comentario inexistente

#     with app.test_request_context():
#         result = delete_review(review_id_to_delete)

#     assert "No se encontró la reseña a eliminar." in result.response.get_data(as_text=True)

# # Test para enviar una reseña
# def test_send_review(mock_reviews, app):
#     mock_reviews['add_review'].return_value = None
#     review_data = {
#         'rating': '5',
#         'comment': 'Excellent tutor!',
#         'student_id': '1',
#         'tutor_id': '2',
#         'session_id': '101',
#         'review_id': '1'
#     }

#     with app.test_request_context(method='POST', data=review_data):
#         result = send_review()

#     mock_reviews['add_review'].assert_called_once_with({
#         'student_id': '1',
#         'tutor_id': '2',
#         'session_id': '101',
#         'rating': 5,
#         'review_id': 1,
#         'comment': 'Excellent tutor!'
#     })
    
#     assert "Reseña enviada correctamente." in result.response.get_data(as_text=True)

# # Test para verificar que un comentario eliminado ya no aparece en el perfil del tutor
# def test_comment_not_appearing_after_deletion(mock_reviews, app):
#     mock_reviews['get_all_reviews'].return_value = [
#         {"review_id": 1, "student_id": 1, "tutor_id": 2, "comment": "Great tutor!", "rating": 5},
#         {"review_id": 2, "student_id": 2, "tutor_id": 2, "comment": "Good explanation.", "rating": 4},
#     ]

#     review_id_to_delete = 1
#     mock_reviews['save_reviews'].return_value = None

#     # Primero eliminamos la reseña
#     with app.test_request_context():
#         delete_review(review_id_to_delete)

#     mock_reviews['get_all_reviews'].return_value = [
#         {"review_id": 2, "student_id": 2, "tutor_id": 2, "comment": "Good explanation.", "rating": 4},
#     ]
    
#     with app.test_request_context():
#         result = get_all_reviews()

#     assert len(result) == 1
#     assert result[0]["review_id"] == 2
#     assert "Great tutor!" not in [r['comment'] for r in result]
