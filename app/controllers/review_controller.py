from flask import request, redirect, flash, abort, session

from app.models.review_model import add_review, get_all_reviews, add_reply_to_review, save_reviews, get_review_by_id, update_review, delete_review as delete_review_model

import logging
from datetime import datetime
from app.controllers.review_presenter_controller import ConsoleReviewPresenter ## Si queremos agregar en un futuro LogFileReviewPresenter, EmailReviewPresenter

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_PRESENTER = ConsoleReviewPresenter()

def send_review(tutor_id=None, session_id=None):
    #Hay que comprobar rol
    #Hay que comprobar que haya llevado la tutoria.
    rating = request.form.get('rating')
    comment = request.form.get('comment', '')

    #student_id = request.form.get('student_id')
    student_id = session.get('name')

    form_tutor_id = request.form.get('tutor_id')
    
    form_session_id = request.form.get('session_id')
    
    review_id = request.form.get('review_id')

    # Se usa el session_id del argumento si se pasa, si no se toma del form
    session_id = session_id or form_session_id
    tutor_id = tutor_id or form_tutor_id

    # Validaciones
    if not rating:
        flash("La calificación no puede estar vacía.", "warning")
        return redirect(request.referrer or f'/comments/{tutor_id}/{session_id}')

    if not rating.isdigit():
        flash("La calificación debe ser un número válido.", "warning")
        return redirect(request.referrer or f'/comments/{tutor_id}/{session_id}')
    
    if not (1 <= int(rating) <= 5):
        flash("La calificación debe estar entre 1 y 5.", "warning")
        return redirect(request.referrer or f'/comments/{tutor_id}/{session_id}')

    if not comment.strip():
        flash("El comentario no puede estar vacío.", "warning")
        return redirect(request.referrer or f'/comments/{tutor_id}/{session_id}')

    # Crear el diccionario de la reseña
    review = {
        "student_id": student_id,
        "tutor_id": tutor_id,
        "session_id": session_id,
        "rating": int(rating),
        "review_id": int(review_id),
        "comment": comment,
        "date": datetime.now().strftime('%d/%m/%Y'),
        "reply": None
    }

    add_review(review)
    DEFAULT_PRESENTER.present_review(review)

    flash("Reseña enviada correctamente", "success")
    return redirect(f"/comments/{tutor_id}/{session_id}")

def delete_review(review_id):
    #Hay que comprobar rol
    #Hay que comprobar que sea el mismo estudiante
    reviews = get_all_reviews()
    review = next((r for r in reviews if r['review_id'] == review_id), None)

    if not review:
        flash("No se encontró la reseña a eliminar.", "warning")
        return redirect("/comments")

    session_id = review['session_id']
    tutor_id = review['tutor_id']
    updated_reviews = [r for r in reviews if r['review_id'] != review_id]
    delete_review_model(review_id)
    save_reviews(updated_reviews)

    flash("Reseña eliminada exitosamente.", "success")
    return redirect(f"/comments/{tutor_id}/{session_id}")


def add_reply(review_id):
    # Hay que comprobar rol
    # Hay que comprobar que sea el mismo tutor
    #try:
        tutor_id = request.form.get('tutor_id')
        comment = request.form.get('comment', '').strip()

        if not comment:
            flash("El comentario no puede estar vacío", "warning")
            return redirect(request.referrer or '/comments')

        if not tutor_id:
            flash("Debes iniciar sesión como tutor para responder", "danger")
            return redirect(request.referrer or '/comments')

        review = get_review_by_id(review_id)
        if not review:
            flash("No se encontró la reseña", "danger")
            return redirect("/comments")

        session_id = review['session_id']
        tutor_id = review['tutor_id']

        if add_reply_to_review(review_id, tutor_id, comment):
            logger.info(f"Respuesta añadida a review {review_id}")
            flash("Respuesta publicada exitosamente", "success")
        else:
            logger.warning(f"Review no encontrada: {review_id}")
            flash("No se encontró la reseña", "danger")
    
        return redirect(f"/comments/{tutor_id}/{session_id}")

    #except Exception as e:
     #   logger.error(f"Error en add_reply: {str(e)}")
      #  flash("Error al procesar tu respuesta", "danger")
       # return redirect("/comments/{tutor_id}/{session_id}")

def edit_review(review_id):
    #Comprobar que sea estudiante
    #Comprobar que sea el mismo
    comment = request.form.get('comment', '').strip()
    rating = request.form.get('rating')

    if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
        flash("Calificación inválida.", "warning")
        return redirect(request.referrer or '/comments')

    review = get_review_by_id(review_id)
    if not review:
        flash("No se encontró la reseña a editar.", "warning")
        return redirect("/comments")

    tutor_id = review['tutor_id']
    session_id = review['session_id']

    if update_review(review_id, int(rating), comment):
        flash("Reseña actualizada correctamente.", "success")
    else:
        flash("No se encontró la reseña a editar.", "warning")


    return redirect(f"/comments/{tutor_id}/{session_id}")

