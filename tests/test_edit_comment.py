import pytest
from datetime import datetime
from app.__init__ import app
from app.models.review_model import save_reviews, _load_reviews

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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

def test_can_edit_existing_review(client, setup_review):
    rv_id = setup_review['review_id']
    response = client.post(f"/edit-review/{rv_id}", data={
        'comment': "Comentario actualizado.",
        'rating': 4
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Comentario actualizado." in response.data

    reviews = _load_reviews()
    updated = next(r for r in reviews if r["review_id"] == rv_id)
    assert updated["comment"] == "Comentario actualizado."
    assert updated["rating"] == 4

def test_edit_button_visible(client, setup_review):
    response = client.get("/comments")
    assert b"Editar" in response.data

def test_can_change_rating(client, setup_review):
    rv_id = setup_review['review_id']
    new_rating = 5

    response = client.post(f"/edit-review/{rv_id}", data={
        'comment': setup_review['comment'],  # dejamos el comentario igual
        'rating': new_rating
    }, follow_redirects=True)

    assert response.status_code == 200
    assert str(new_rating).encode() in response.data  # Verificamos que la nueva calificación aparece en la respuesta

    reviews = _load_reviews()
    updated = next(r for r in reviews if r["review_id"] == rv_id)
    assert updated["rating"] == new_rating