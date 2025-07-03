from flask import request, redirect, flash, abort, session

from app.models.review_model import add_review, get_all_reviews, add_reply_to_review, save_reviews, get_review_by_id, update_review, delete_review as delete_review_model

import logging
from datetime import datetime
from app.controllers.review_presenter_controller import ConsoleReviewPresenter, EmailReviewPresenter ## Si queremos agregar en un futuro LogFileReviewPresenter
#from better_profanity import profanity
import os
import re

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_PRESENTER = ConsoleReviewPresenter()
EMAIL_PRESENTER = EmailReviewPresenter()

def send_review(tutoria=None):
    
    # Hay que comprobar rol
    tutor_id = tutoria.tutor
    session_id = tutoria.title
    tutoria_id = tutoria.id
    
    if session.get('role') != 'Student':
        flash("Debes ser un estudiante para dejar una critica.", "danger")
        return redirect(request.referrer or f'/comments/{tutoria_id}')


    # Hay que comprobar que haya llevado la tutoria.
    student_id = session.get('name')
    enrolled = tutoria.student_list
    exists = next((s for s in enrolled if s['name'] == student_id), None)

    if not exists:
        flash("No estas inscrito en esta tutoría. No puedes enviar una critica.", "danger")
        return redirect(f"/comments/{tutoria_id}")


    rating = request.form.get('rating')
    comment = request.form.get('comment', '')
    review_id = request.form.get('review_id')
    drive_link = request.form.get('drive_link', '').strip()


    # Validaciones
    if not rating:
        flash("La calificación no puede estar vacía.", "danger")
        return redirect(request.referrer or f'/comments/{tutoria_id}')

    if not rating.isdigit():
        flash("La calificación debe ser un número válido.", "danger")
        return redirect(request.referrer or f'/comments/{tutoria_id}')
    
    if not (1 <= int(rating) <= 5):
        flash("La calificación debe estar entre 1 y 5.", "danger")
        return redirect(request.referrer or f'/comments/{tutoria_id}')

    if not comment.strip():
        flash("El comentario no puede estar vacío.", "warning")
        return redirect(request.referrer or f'/comments/{tutoria_id}')
    
    if is_injection(comment):
        flash("El comentario contiene patrones de inyección de código y fue bloqueado.", "danger")
        return redirect(request.referrer or f'/comments/{tutoria_id}')
    
    if is_offensive(comment):
        flash("El comentario contiene lenguaje ofensivo y no puede ser enviado.", "danger")
        return redirect(request.referrer or f'/comments/{tutoria_id}')

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
    
    # Notify all presenters (console and email)
    DEFAULT_PRESENTER.present_review(review)
    EMAIL_PRESENTER.present_review(review)

    flash("Reseña enviada correctamente", "success")
    return redirect(f"/comments/{tutoria_id}")

def delete_review(tutoria_id, review_id):
    
    reviews = get_all_reviews()
    review = next((r for r in reviews if r['review_id'] == review_id), None)

    if not review:
        flash("No se encontró la reseña a eliminar.", "warning")
        return redirect(f"/comments/{tutoria_id}")
    
    # Hay que comprobar rol
    if session.get('role') == 'Student':
        # Hay que comprobar que sea el mismo estudiante
        if session.get('name') != review['student_id']:
            flash("No puedes eliminar la critica de otro estudiante.", "warning")
            return redirect(f"/comments/{tutoria_id}")
        
    if session.get('role') == 'Tutor':
        # Hay que comprobar que sea el mismo tutor
        if session.get('name') != review['tutor_id']:
            flash("No puedes eliminar una critica de un perfil ajeno.", "warning")
            return redirect(f"/comments/{tutoria_id}")

    updated_reviews = [r for r in reviews if r['review_id'] != review_id]
    delete_review_model(review_id)
    save_reviews(updated_reviews)
    
    logger.info(f"La review {review_id} fue eliminada por el {session.get('role')}: {session.get('name')}")
    flash("Reseña eliminada exitosamente.", "success")
    return redirect(f"/comments/{tutoria_id}")

def add_reply(tutoria_id, review_id):
    tutor_id = request.form.get('tutor_id')
    comment = request.form.get('comment', '').strip()
    drive_link = request.form.get('drive_link', '').strip()

    review = get_review_by_id(review_id)
    if not review:
        flash("No se encontró la reseña", "danger")
        return redirect(f"/comments/{tutoria_id}")

    # Hay que comprobar rol
    if session.get('role') != 'Tutor' :
        flash("No puedes responder, no eres tutor.", "warning")
        return redirect(f"/comments/{tutoria_id}")

    # Hay que comprobar que sea el mismo tutor
    if session.get('name') != review['tutor_id'] :
        flash("No puedes responder, no son tus criticas.", "warning")
        return redirect(f"/comments/{tutoria_id}")

    tutor_id = session.get('name')
    comment = request.form.get('comment', '').strip()

    if not comment:
        flash("El comentario no puede estar vacío", "warning")
        return redirect(request.referrer or f"/comments/{tutoria_id}")
    
    if is_injection(comment):
        flash("El comentario contiene patrones de inyección de código y fue bloqueado.", "danger")
        return redirect(request.referrer or f'/comments/{tutoria_id}')
    
    if is_offensive(comment):
        flash("El comentario contiene lenguaje ofensivo y no puede ser enviado.", "danger")
        return redirect(request.referrer or f'/comments/{tutoria_id}')

    if add_reply_to_review(review_id, tutor_id, comment, drive_link):
        logger.info(f"Respuesta añadida a review {review_id}")
        
        # Create reply data for email notification
        reply_data = {
            'is_reply': True,
            'student_id': review['student_id'],  # The original commenter (student)
            'tutor_id': tutor_id,  # The tutor who replied
            'comment': comment,  # The reply text
            'session_id': review['session_id'],  # The tutorial name
            'original_comment': review['comment']  # The original comment
        }
        
        EMAIL_PRESENTER.present_review(reply_data)
        
        flash("Respuesta publicada exitosamente", "success")
    else:
        logger.warning(f"Review no encontrada: {review_id}")
        flash("No se encontró la reseña", "danger")

    return redirect(f"/comments/{tutoria_id}")


def edit_review(tutoria_id, review_id):
    
    review = get_review_by_id(review_id)
    if not review:
        flash("No se encontró la reseña a editar.", "warning")
        return redirect(f"/comments/{tutoria_id}")
    
    # Comprobar que sea estudiante y Comprobar que sea el mismo
    if session.get('role') != 'Student' or session.get('name') != review['student_id'] :
        flash("No puedes editar esta critica, no es tuya.", "warning")
        return redirect(f"/comments/{tutoria_id}")

    comment = request.form.get('comment', '').strip()
    rating = request.form.get('rating')
    drive_link = request.form.get('drive_link', '').strip()

    if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
        flash("Calificación inválida.", "warning")
        return redirect(request.referrer or f"/comments/{tutoria_id}")
    
    if is_injection(comment):
        flash("El comentario contiene patrones de inyección de código y fue bloqueado.", "danger")
        return redirect(request.referrer or f'/comments/{tutoria_id}')

    if is_offensive(comment):
        flash("El comentario contiene lenguaje ofensivo y no puede ser enviado.", "danger")
        return redirect(request.referrer or f'/comments/{tutoria_id}')

    review['comment'] = comment
    review['rating'] = int(rating)
    review['drive_link'] = drive_link

    update_review(review_id, review['rating'], review['comment'], drive_link)

    flash("Reseña actualizada correctamente.", "success")
    return redirect(f"/comments/{tutoria_id}")

def edit_reply(tutoria_id, review_id, reply_index):
    review = get_review_by_id(review_id)
    comment = request.form.get('comment', '').strip()
    drive_link = request.form.get('drive_link', '').strip()

    if session.get('role') != 'Tutor' or session.get('name') != review['tutor_id'] :
        flash("No puedes editar esta critica, no es tuya.", "warning")
        return redirect(f"/comments/{tutoria_id}")
    
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

    return redirect(f"/comments/{tutoria_id}")

def delete_reply(tutoria_id, review_id, reply_index):
    review = get_review_by_id(review_id)
    if not review:
        flash("No se encontró la reseña.", "danger")
        return redirect("/comments")
    
    session_id = review.get("session_id", "")

    if session.get('name') != review['tutor_id']:
            flash("No puedes eliminar la critica de un tutor.", "warning")
            return redirect(f"/comments/{tutoria_id}")
    
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

    return redirect(f"/comments/{tutoria_id}")

def calculate_average_tutor(tutor_id):
    all_reviews = get_all_reviews()
    tutor_reviews = [r for r in all_reviews if r['tutor_id'] == tutor_id]
    return calculate_average_reviews(tutor_reviews)

def calculate_average_tutoring(tutor_id, tutoring_id):
    all_reviews = get_all_reviews()
    tutor_reviews = [r for r in all_reviews if r['tutor_id'] == tutor_id and r['session_id'] == tutoring_id]
    return calculate_average_reviews(tutor_reviews)

def calculate_average_reviews(reviews):
    if not reviews:
        return 0  # Evita división por cero

    suma = sum(int(r['rating']) for r in reviews)
    average = suma / len(reviews)
    return round(average, 2)

def init_word_filter():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(os.path.join(base_dir, '..', 'utils', 'offensive_words_es.txt'))

    with open(file_path, encoding="utf-8") as f:
        words_es = [str(line.strip()) for line in f if line.strip()]

    words_en = [str(word) for word in profanity.CENSOR_WORDSET]
    profanity.load_censor_words(words_es + words_en)

def is_offensive(comment):
    init_word_filter()
    comment = comment.lower()
    return profanity.contains_profanity(comment)

def is_injection(comment):
    comment = comment.lower()

    suspicious_patterns = [
        r"('|--|;)",                     # SQL básico
        r"(drop\s+table|insert\s+into|select\s+.+\s+from)",  # SQL avanzado
        r"<script.*?>.*?</script>",     # XSS básico
        r"(onerror\s*=|onload\s*=)",    # JS embebido
        r"(alert\s*\(|confirm\s*\()",   # JS funciones comunes
        r"`.*?`",                        # command injection
        r"\$\{.*?\}",                   # template injection
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, comment):
            return True
    return False
