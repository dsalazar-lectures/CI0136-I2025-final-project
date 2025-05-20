import pytest
from datetime import datetime, timedelta
from app.app import app as flask_app
from app.models.review_model import save_reviews, _load_reviews

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    return flask_app.test_client()

@pytest.fixture
def setup_review():
    review = {
        "student_id": "EstudianteTest",
        "tutor_id": "TutorTest",
        "session_id": "Sesion de Python",
        "review_id": 99999,
        "rating": 3,
        "comment": "Comentario original.",
        "date": datetime.now().strftime("%d/%m/%Y")
    }
    save_reviews([review])
    return review

# def test_can_edit_existing_review(client, setup_review):
#     """Dado que ya dejé un comentario, puedo editarlo y se muestra actualizado"""
#     rv_id = setup_review['review_id']
#     response = client.post(f"/edit-review/{rv_id}", data={
#         'comment': "Comentario actualizado.",
#         'rating': 4
#     }, follow_redirects=True)

#     assert response.status_code == 200
#     assert b"Comentario actualizado." in response.data

#     reviews = _load_reviews()
#     updated = next(r for r in reviews if r["review_id"] == rv_id)
#     assert updated["comment"] == "Comentario actualizado."
#     assert updated["rating"] == 4

# def test_edit_button_visible(client, setup_review):
#     """Dado que publiqué un comentario, puedo ver el botón Editar en el perfil"""
#     response = client.get("/")
#     assert b"Editar" in response.data

