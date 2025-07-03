from abc import ABC, abstractmethod
import logging
from datetime import datetime
from app.services.notification import send_email_notification
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository

## Clase abstracta presentadora de reviews
class ReviewPresenterStrategy(ABC):
    
    @abstractmethod
    def present_review(self, review):
        pass

class ConsoleReviewPresenter(ReviewPresenterStrategy):
    def present_review(self, review):
        print("\n--- Nueva Reseña Recibida ---")
        print(f"\tEstudiante: {review['student_id']}")
        print(f"\tTutor ID: {review['tutor_id']}")
        print(f"\tSesión ID: {review['session_id']}")
        print(f"\tReview ID: {review['review_id']}")
        print(f"\tEstrellas: {review['rating']}")
        print(f"\tComentario: {review['comment']}")
        if review.get('drive_link'):
            print(f"\tLink de Drive: {review['drive_link']}")
        print("------------------------------\n")

class LogFileReviewPresenter(ReviewPresenterStrategy):
    ## Se cambia a los logs creados por nosotros
    def __init__(self, logger=None):
        if logger is None:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger
    
    def present_review(self, review):
        ## Si se quiere loggear
        pass

class EmailReviewPresenter(ReviewPresenterStrategy):

    def __init__(self):
        self.user_repo = FirebaseUserRepository()
        
    def present_review(self, review):
        """
        Envía notificaciones por email cuando se crea o responde a un comentario
        """
        try:
            # Determinar si es un comentario nuevo o una respuesta
            if 'is_reply' in review and review['is_reply']:
                self._send_tutor_reply_notification(review)
            else:
                self._send_new_comment_notification(review)
        except Exception as e:
            print(f"Error sending email notification: {e}")
    def _send_new_comment_notification(self, review):
        """
        Envía notificación al tutor cuando recibe un comentario nuevo
        """
        tutor_name = review.get('tutor_id', '')
        student_name = review.get('student_id', '')
        
        # Obtener email del tutor
        tutor_data = self.user_repo.get_user_by_name(tutor_name)
        if not tutor_data or not tutor_data.get('email'):
            print(f"No se pudo obtener el email del tutor: {tutor_name}")
            return
        
        # Verificar si el tutor tiene notificaciones habilitadas
        if not tutor_data.get('notification_enabled', True):
            print(f"Tutor {tutor_name} tiene notificaciones deshabilitadas")
            return

        email_data = {
            "username": tutor_name,
            "emailTo": tutor_data['email'],
            "student_name": student_name,
            "comment": review.get('comment', ''),
            "rating": review.get('rating', 0),
            "tutorial": review.get('session_id', '')
        }

        success = send_email_notification("newComment", email_data)
        if success:
            print(f"Email notification sent to tutor {tutor_name}")
        else:
            print(f"Failed to send email notification to tutor {tutor_name}")

    def _send_tutor_reply_notification(self, review):
        """
        Envía notificación al estudiante cuando el tutor responde
        """
        student_name = review.get('student_id', '')
        tutor_name = review.get('tutor_id', '')
        
        # Obtener email del estudiante
        student_data = self.user_repo.get_user_by_name(student_name)
        if not student_data or not student_data.get('email'):
            print(f"No se pudo obtener el email del estudiante: {student_name}")
            return
        
        # Verificar si el estudiante tiene notificaciones habilitadas
        if not student_data.get('notification_enabled', True):
            print(f"Estudiante {student_name} tiene notificaciones deshabilitadas")
            return

        email_data = {
            "username": student_name,
            "emailTo": student_data['email'],
            "tutor_name": tutor_name,
            "reply": review.get('comment', ''),
            "tutorial": review.get('session_id', ''),
            "original_comment": review.get('original_comment', '')
        }

        success = send_email_notification("tutorReply", email_data)
        if success:
            print(f"Email notification sent to student {student_name}")
        else:
            print(f"Failed to send email notification to student {student_name}")