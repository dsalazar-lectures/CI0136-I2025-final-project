from datetime import datetime
from app.services.notification import send_email_notification
from app.services.audit import log_audit, AuditActionType
from app.models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository

class TutoringRemember:
    def __init__(self, tutoring_repo : FirebaseTutoringRepository, user_repo: FirebaseUserRepository):
        """
        Initialize the recommender with a tutoring repository.
        Args:
            tutoring_repo (TutoringRepository): Repository to fetch tutorings.
        """
        self.tutoring_repo = tutoring_repo
        self.user_repo = user_repo

    def send_tutoring_reminder(self, next_minutes=30):
        """
        Remember future tutorings for students.
        """

        next_tutorings = []
        for t in self.tutoring_repo.get_list_tutorials():
            date_part = datetime.strptime(t.date, "%Y-%m-%d").date()
            time_part = datetime.strptime(t.start_time, "%H:%M").time()
            tutoring_datetime = datetime.combine(date_part, time_part)

            if tutoring_datetime > datetime.now():
                seconds_until_tutoring = (tutoring_datetime - datetime.now()).total_seconds()
                if seconds_until_tutoring <= next_minutes * 60:
                    next_tutorings.append(t)
        email_type = "reminder"
        for tutoring in next_tutorings:
            for student in tutoring.student_list:
                id = student["id"]
                user = self.user_repo.get_user_by_id(student["id"])
                date_part = datetime.strptime(tutoring.date, "%Y-%m-%d").date()
                time_part = datetime.strptime(tutoring.start_time, "%H:%M").time()
                tutoring_datetime = datetime.combine(date_part, time_part)

                email_data = {
                    "username": user["name"],
                    "emailTo": user["email"],
                    "tutoringTitle": tutoring.title,
                    "tutoringDateTime": tutoring_datetime
                }
                if not send_email_notification(email_type, email_data):
                    log_audit(
                        user = student.name,
                        action_type = AuditActionType.EMAIL_NOTIFICATION,
                        details = "Failed to send confirmation email",
                    )
