from flask import request, session, redirect, flash, abort
from models.review_model import add_review, get_all_reviews


def send_review():
    rating = request.form.get('rating')
    comment = request.form.get('comment', '')
    student_id = request.form.get('student_id')
    tutor_id = request.form.get('tutor_id')
    session_id =  request.form.get('session_id')

    if not rating:
        flash("Calificacion invalida, la calificacion no puede estar vacia.", "warning")
        abort(400)

    if not rating.isdigit():
        flash("Calificacion invalida, la calificacion debe ser un digito.", "warning")
        abort(400)

    if not (1 <= int(rating) <= 5):
        flash("Calificacion invalida, la calificacion debe estar entre 1 y 5.", "warning")
        abort(400)

    review = {
        "student_id": student_id,
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
    print(f"\tSesion ID: {review['session_id']}")
    print(f"\tEstrellas: {review['rating']}")
    print(f"\tComentario: {review['comment']}")
    print("------------------------------\n")