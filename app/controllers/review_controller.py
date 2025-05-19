<<<<<<< HEAD
from flask import request, session, redirect

REVIEWS_MOCK = []

def send_review():
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    tutor_id = request.form.get('tutor_id')
    session_id =  request.form.get('session_id')

    review = {
        "student_id": "estudiantePrueba",
        "tutor_id": tutor_id,
        "session_id": session_id,
        "rating": int(rating),
        "comment": comment
    }

    REVIEWS_MOCK.append(review)

    print_resena(review)
    return redirect("/")

def print_resena(review):
    print("\n--- Nueva Resena Recibida ---")
    print(f"\tEstudiante: {review['student_id']}")
    print(f"\tTutor ID: {review['tutor_id']}")
    print(f"\tSesión ID: {review['session_id']}")
    print(f"\tEstrellas: {'★' * review['rating']}{'☆' * (5 - review['rating'])}")
    print(f"\tComentario: {review['comment']}")
    print("------------------------------\n")
=======
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
    
    if not rating:
        flash("Calificación inválida, la calificación no puede estar vacía.", "warning")
        abort(400)
    
    if not rating.isdigit():
        flash("Calificación inválida, la calificación debe ser un dígito.", "warning")
        abort(400)
    
    if not (1 <= int(rating) <= 5):
        flash("Calificación inválida, debe estar entre 1 y 5.", "warning")
        abort(400)
    
    review = {
        "student_id": student_id,
        "tutor_id": tutor_id,
        "session_id": session_id,
        "rating": int(rating),
        "review_id": int(review_id),
        "comment": comment
    }
    
    add_review(review)
    
    # Utilizamos la estrategia de presentación configurada por el momento
    DEFAULT_PRESENTER.present_review(review)
    
    return redirect("/")

def delete_review(review_id):
    reviews = get_all_reviews()
    updated_reviews = [r for r in reviews if r['review_id'] != review_id]
    
    if len(updated_reviews) < len(reviews):
        save_reviews(updated_reviews)
        flash("Reseña eliminada exitosamente.", "success")
    else:
        flash("No se encontró la reseña a eliminar.", "warning")
    
    return redirect("/")

def add_reply(review_id):
    try:
        tutor_id = request.form.get('tutor_id')
        comment = request.form.get('comment', '').strip()
        
        if not comment:
            flash("El comentario no puede estar vacío", "warning")
            return redirect(request.referrer or '/')
        
        if not tutor_id:
            flash("Debes iniciar sesión como tutor para responder", "danger")
            return redirect(request.referrer or '/')
        
        if add_reply_to_review(review_id, tutor_id, comment):
            logger.info(f"Respuesta añadida a review {review_id}")
            flash("Respuesta publicada exitosamente", "success")
        else:
            logger.warning(f"Review no encontrada: {review_id}")
            flash("No se encontró la reseña", "danger")
        
        return redirect(request.referrer or '/')
    
    except Exception as e:
        logger.error(f"Error en add_reply: {str(e)}")
        flash("Error al procesar tu respuesta", "danger")
        return redirect(request.referrer or '/')
    
def edit_review(review_id):
    comment = request.form.get('comment', '').strip()
    rating = request.form.get('rating')

    if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
        flash("Calificación inválida.", "warning")
        return redirect(request.referrer or '/')

    from app.models.review_model import update_review

    if update_review(review_id, int(rating), comment):
        flash("Reseña actualizada correctamente.", "success")
    else:
        flash("No se encontró la reseña a editar.", "warning")
    
    return redirect('/')
>>>>>>> feature/review_pop-up
