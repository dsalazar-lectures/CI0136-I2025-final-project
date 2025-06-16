from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository
from app.models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository
from app.models.review_model import get_all_reviews

def get_admin_metrics():
    user_repo = FirebaseUserRepository()
    tutorial_repo = FirebaseTutoringRepository()

    # Users
    users = user_repo.get_all_users()
    total_users = len(users)
    students = [u for u in users if u.get('role') == 'Student']
    tutors = [u for u in users if u.get('role') == 'Tutor']
    admins = [u for u in users if u.get('role') in ('Admin', 'Administrator')]
    total_students = len(students)
    total_tutors = len(tutors)
    total_admins = len(admins)

    # Tutorials
    tutorials = tutorial_repo.get_list_tutorials()
    total_tutorials = len(tutorials)
    total_enrollments = sum(len(t.student_list) for t in tutorials)

    # Reviews
    reviews = get_all_reviews()
    total_reviews = len(reviews)

    return {
        'total_users': total_users,
        'total_students': total_students,
        'total_tutors': total_tutors,
        'total_admins': total_admins,
        'total_tutorials': total_tutorials,
        'total_enrollments': total_enrollments,
        'total_reviews': total_reviews
    }
