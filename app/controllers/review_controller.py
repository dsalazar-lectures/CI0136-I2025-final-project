from flask import request, redirect, flash, abort

from app.models.review_model import add_review, get_all_reviews, add_reply_to_review, save_reviews, get_review_by_id, update_review, delete_review as delete_review_model

import logging
from datetime import datetime
from app.controllers.review_presenter_controller import ConsoleReviewPresenter ## Si queremos agregar en un futuro LogFileReviewPresenter, EmailReviewPresenter

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_PRESENTER = ConsoleReviewPresenter()

def send_review(session_id=None):
    rating = request.form.get('rating')
    comment = request.form.get('comment', '')
    student_id = request.form.get('student_id')
    tutor_id = request.form.get('tutor_id')
    form_session_id = request.form.get('session_id')
    review_id = request.form.get('review_id')
    drive_link = request.form.get('drive_link', '').strip()

    # Se usa el session_id del argumento si se pasa, si no se toma del form
    session_id = session_id or form_session_id

    # Validaciones
    if not rating:
        flash("La calificación no puede estar vacía.", "warning")
        return redirect(request.referrer or f'/comments/{session_id}')

    if not rating.isdigit():
        flash("La calificación debe ser un número válido.", "warning")
        return redirect(request.referrer or f'/comments/{session_id}')
    
    if not (1 <= int(rating) <= 5):
        flash("La calificación debe estar entre 1 y 5.", "warning")
        return redirect(request.referrer or f'/comments/{session_id}')

    if not comment.strip():
        flash("El comentario no puede estar vacío.", "warning")
        return redirect(request.referrer or f'/comments/{session_id}')

    # Crear el diccionario de la reseña
    review = {
        "student_id": student_id,
        "tutor_id": tutor_id,
        "session_id": session_id,
        "rating": int(rating),
        "review_id": int(review_id),
        "comment": comment,
        "drive_link": drive_link,
        "date": datetime.now().strftime('%d/%m/%Y'),
        "reply": None
    }

    add_review(review)
    DEFAULT_PRESENTER.present_review(review)

    flash("Reseña enviada correctamente", "success")
    return redirect(f"/comments/{session_id}")

def delete_review(review_id):

    reviews = get_all_reviews()
    review = next((r for r in reviews if r['review_id'] == review_id), None)

    if not review:
        flash("No se encontró la reseña a eliminar.", "warning")
        return redirect("/comments")

    session_id = review['session_id']
    updated_reviews = [r for r in reviews if r['review_id'] != review_id]
    delete_review_model(review_id)
    save_reviews(updated_reviews)

    flash("Reseña eliminada exitosamente.", "success")
    return redirect(f"/comments/{session_id}")

def add_reply(review_id):
    session_id = None

    try:
        tutor_id = request.form.get('tutor_id')
        comment = request.form.get('comment', '').strip()
        drive_link = request.form.get('drive_link', '').strip()

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

        session_id = review.get('session_id')

        if add_reply_to_review(review_id, tutor_id, comment, drive_link):
            logger.info(f"Respuesta añadida a review {review_id}")
            flash("Respuesta publicada exitosamente", "success")
        else:
            logger.warning(f"Review no encontrada: {review_id}")
            flash("No se encontró la reseña", "danger")

        return redirect(f"/comments/{session_id}")

    except Exception as e:
        logger.error(f"Error en add_reply: {str(e)}")
        flash("Error al procesar tu respuesta", "danger")
        if session_id:
            return redirect(f"/comments/{session_id}")
        else:
            return redirect("/comments")

def edit_review(review_id):
    comment = request.form.get('comment', '').strip()
    rating = request.form.get('rating')
    drive_link = request.form.get('drive_link', '').strip()

    if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
        flash("Calificación inválida.", "warning")
        return redirect(request.referrer or '/comments')

    review = get_review_by_id(review_id)
    if not review:
        flash("No se encontró la reseña a editar.", "warning")
        return redirect("/comments")

    session_id = review['session_id']

    review['comment'] = comment
    review['rating'] = int(rating)
    review['drive_link'] = drive_link

    update_review(review_id, review['rating'], review['comment'], drive_link)

    flash("Reseña actualizada correctamente.", "success")
    return redirect(f"/comments/{session_id}")

def edit_reply(review_id, reply_index):
    comment = request.form.get('comment', '').strip()
    drive_link = request.form.get('drive_link', '').strip()

    if not comment:
        flash("El comentario no puede estar vacío.", "warning")
        return redirect(request.referrer or "/comments")

    review = get_review_by_id(review_id)
    if not review:
        flash("No se encontró la reseña original.", "danger")
        return redirect("/comments")

    session_id = review.get("session_id", "")

    try:
        replies = review.get("replies", [])
        if 0 <= reply_index < len(replies):
            replies[reply_index]['comment'] = comment
            replies[reply_index]['drive_link'] = drive_link
            replies[reply_index]['date'] = datetime.now().strftime('%d/%m/%Y')

            save_reviews(get_all_reviews())
            # Update Firestore
            from app.models.review_model import save_review_to_firestore
            save_review_to_firestore(review)

            flash("Respuesta editada exitosamente.", "success")
        else:
            flash("Índice de respuesta no válido.", "danger")
    except Exception as e:
        logger.error(f"Error al editar respuesta: {e}")
        flash("Error al editar la respuesta.", "danger")

    return redirect(f"/comments/{session_id}")

def delete_reply(review_id, reply_index):
    review = get_review_by_id(review_id)
    if not review:
        flash("No se encontró la reseña.", "danger")
        return redirect("/comments")

    session_id = review.get("session_id", "")
    try:
        replies = review.get("replies", [])
        if 0 <= reply_index < len(replies):
            deleted = replies.pop(reply_index)

            save_reviews(get_all_reviews())
            from app.models.review_model import save_review_to_firestore
            save_review_to_firestore(review)

            flash("Respuesta eliminada exitosamente.", "success")
        else:
            flash("Índice de respuesta no válido.", "danger")
    except Exception as e:
        logger.error(f"Error al eliminar respuesta: {e}")
        flash("Error al eliminar la respuesta.", "danger")

    return redirect(f"/comments/{session_id}")
