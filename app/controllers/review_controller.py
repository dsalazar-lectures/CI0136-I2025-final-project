from flask import request, redirect, flash, abort
from app.models.review_model import add_review, get_all_reviews, add_reply_to_review, save_reviews, get_review_by_id
import logging
from datetime import datetime
from app.controllers.review_presenter_controller import ConsoleReviewPresenter ## Si queremos agregar en un futuro LogFileReviewPresenter, EmailReviewPresenter


# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_PRESENTER = ConsoleReviewPresenter()

def send_review():
    rating = request.form.get('rating')
    comment = request.form.get('comment', '')
    student_id = request.form.get('student_id')
    tutor_id = request.form.get('tutor_id')
    session_id = request.form.get('session_id')
    review_id = request.form.get('review_id')

    # Verificar que la calificación no esté vacía
    if not rating:
        flash("La calificación no puede estar vacía.", "warning")
        return redirect(request.referrer or '/comments')

    # Verificar que la calificación sea un número y esté en el rango válido
    if not rating.isdigit():
        flash("La calificación debe ser un número válido.", "warning")
        return redirect(request.referrer or '/comments')
    
    if not (1 <= int(rating) <= 5):
        flash("La calificación debe estar entre 1 y 5.", "warning")
        return redirect(request.referrer or '/comments')

    # Verificar que el comentario no esté vacío
    if not comment.strip():
        flash("El comentario no puede estar vacío.", "warning")
        return redirect(request.referrer or '/comments')

    # Crear el diccionario de la reseña
    review = {
        "student_id": student_id,
        "tutor_id": tutor_id,
        "session_id": session_id,
        "rating": int(rating),
        "review_id": int(review_id),
        "comment": comment
    }

    # Guardar la reseña
    add_review(review)

    # Utilizar la estrategia de presentación configurada por el momento
    DEFAULT_PRESENTER.present_review(review)
    
    flash("Reseña enviada correctamente", "success")
    return redirect("/comments")

def delete_review(review_id):
    reviews = get_all_reviews()
    updated_reviews = [r for r in reviews if r['review_id'] != review_id]
    
    if len(updated_reviews) < len(reviews):
        save_reviews(updated_reviews)
        flash("Reseña eliminada exitosamente.", "success")
    else:
        flash("No se encontró la reseña a eliminar.", "warning")
    
    return redirect("/comments")

def add_reply(review_id):
    try:
        tutor_id = request.form.get('tutor_id')
        comment = request.form.get('comment', '').strip()
        
        if not comment:
            flash("El comentario no puede estar vacio", "warning")
            return redirect(request.referrer or '/comments')
        
        if not tutor_id:
            flash("Debes iniciar sesión como tutor para responder", "danger")
            return redirect(request.referrer or '/comments')
        
        if add_reply_to_review(review_id, tutor_id, comment):
            logger.info(f"Respuesta añadida a review {review_id}")
            flash("Respuesta publicada exitosamente", "success")
        else:
            logger.warning(f"Review no encontrada: {review_id}")
            flash("No se encontró la reseña", "danger")
        
        return redirect(request.referrer or '/comments')
    
    except Exception as e:
        logger.error(f"Error en add_reply: {str(e)}")
        flash("Error al procesar tu respuesta", "danger")
        return redirect(request.referrer or '/comments')
    
def edit_review(review_id):
    comment = request.form.get('comment', '').strip()
    rating = request.form.get('rating')

    if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
        flash("Calificación inválida.", "warning")
        return redirect(request.referrer or '/comments')

    from app.models.review_model import update_review

    if update_review(review_id, int(rating), comment):
        flash("Reseña actualizada correctamente.", "success")
    else:
        flash("No se encontró la reseña a editar.", "warning")
    
    return redirect('/comments')