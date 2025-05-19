from abc import ABC, abstractmethod
import logging
from datetime import datetime

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

    def __init__(self, recipient_email="admin@example.com"):
        self.recipient_email = recipient_email
        
    def present_review(self, review):
        ## Si se quiere mandar por email
        pass