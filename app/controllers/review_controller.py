from flask import request, session, redirect
from models.review_model import add_review, get_all_reviews


def send_review():
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    tutor_id = request.form.get('tutor_id')
    session_id =  request.form.get('session_id')

    review = {
        "student_id": "Estudiante Prueba",
        "tutor_id": tutor_id,
        "session_id": session_id,
        "rating": int(rating),
        "comment": comment
    }

    add_review(review)

    print_resena(review)
    return redirect("/")

def print_resena(review):
    print("\n--- Nueva Resena Recibida ---")
    print(f"\tEstudiante: {review['student_id']}")
    print(f"\tTutor ID: {review['tutor_id']}")
    print(f"\tSesión ID: {review['session_id']}")
    print(f"\tEstrellas: {review['rating']}")
    print(f"\tComentario: {review['comment']}")
    print("------------------------------\n")