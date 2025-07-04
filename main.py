from scheduler_service.i_scheduler import IScheduler
from scheduler_service.aps_scheduler import APScheduler
from scheduler_service.tutoring_remember import TutoringRemember
from app.models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository
def main():
    tutoring_repo = FirebaseTutoringRepository()
    user_repo = FirebaseUserRepository()
    scheduler = APScheduler()
    # Register the TutoringRemember service
    tutoring_remember_service = TutoringRemember(tutoring_repo, user_repo)
    
    # Schedule the tutoring reminder task
    scheduler.schedule_task(
        task=tutoring_remember_service.send_tutoring_reminder,
        interval=30 # Interval in minutes
    )

    scheduler.start()
    

if __name__ == "__main__":
    main()
