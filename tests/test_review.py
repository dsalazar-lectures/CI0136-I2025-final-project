import pytest
from app import app  # ✅ importa directamente la instancia
from app.models import review_model

@pytest.fixture
def client(monkeypatch, tmp_path):
    # redirigir el archivo JSON a uno temporal
    test_file = tmp_path / "test_reviews_data.json"
    monkeypatch.setattr(review_model, "JSON_PATH", test_file)

    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_send_review(client):
    review_data = {
        "student_id": "EstudianteTest",
        "tutor_id": "TutorTest",
        "session_id": "Sesion de Prueba",
        "review_id": 11111,
        "rating": "4",
        "comment": "Muy buena tutoría"
    }

    res = client.post("/send-review/Sesion de Prueba", data=review_data, follow_redirects=True)
    assert res.status_code == 200
    assert "Reseña enviada correctamente" in res.get_data(as_text=True)

    reviews = review_model.get_all_reviews()
    assert any(r["review_id"] == 11111 for r in reviews)

def test_filter_reviews_by_session(client):
    review_model.save_reviews([
        {
            "student_id": "A",
            "tutor_id": "T1",
            "session_id": "Sesion A",
            "review_id": 1,
            "rating": 5,
            "comment": "Buenísimo",
            "date": "01/01/2025"
        },
        {
            "student_id": "B",
            "tutor_id": "T2",
            "session_id": "Sesion B",
            "review_id": 2,
            "rating": 4,
            "comment": "Regular",
            "date": "01/01/2025"
        }
    ])

    res = client.get("/comments/Sesion A")
    html = res.get_data(as_text=True)
    assert res.status_code == 200
    assert "Buenísimo" in html
    assert "Regular" not in html

def test_delete_review(client):
    review_model.save_reviews([
        {
            "student_id": "C",
            "tutor_id": "T3",
            "session_id": "Sesion Delete",
            "review_id": 333,
            "rating": 3,
            "comment": "Borrar esto",
            "date": "01/01/2025"
        }
    ])

    res = client.post("/delete-review/333", follow_redirects=True)
    assert res.status_code == 200
    assert "Reseña eliminada exitosamente" in res.get_data(as_text=True)

    reviews = review_model.get_all_reviews()
    assert all(r["review_id"] != 333 for r in reviews)

def test_add_reply(client):
    review_model.save_reviews([
        {
            "student_id": "D",
            "tutor_id": "T4",
            "session_id": "Sesion Respuesta",
            "review_id": 444,
            "rating": 5,
            "comment": "Esperando respuesta",
            "date": "01/01/2025"
        }
    ])

    reply_data = {
        "tutor_id": "T4",
        "comment": "Gracias por tu comentario"
    }

    res = client.post("/reply-review/444", data=reply_data, follow_redirects=True)
    assert res.status_code == 200
    assert "Respuesta publicada exitosamente" in res.get_data(as_text=True)

    review = review_model.get_review_by_id(444)
    assert "replies" in review
    assert len(review["replies"]) == 1
    assert review["replies"][0]["comment"] == "Gracias por tu comentario"
