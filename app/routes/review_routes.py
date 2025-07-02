from flask import Blueprint, render_template, flash
from app.models.review_model import get_all_reviews
from app.controllers.review_controller import send_review, delete_review, add_reply, edit_review, edit_reply, delete_reply, calculate_average_reviews
from app.models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/comments/')
def home():
    user_repo = FirebaseUserRepository()
    comments = get_all_reviews()
    
    # Enrich comments with user profile pictures
    for comment in comments:
        # Get student profile picture
        student_name = comment.get('student_id', '')
        print(f"Processing student: {student_name}")
        try:
            student_data = user_repo.get_user_by_name(student_name)
            student_profile_pic = student_data.get('profile_picture_url', '') if student_data else ''
            comment['student_profile_picture'] = student_profile_pic
            print(f"Student data for {student_name}: {student_data}")
            print(f"Student profile picture: {student_profile_pic}")
        except Exception as e:
            print(f"Error fetching student profile picture for {student_name}: {e}")
            comment['student_profile_picture'] = ''
        
        # Get tutor profile picture for replies
        if 'replies' in comment:
            for reply in comment['replies']:
                tutor_name = reply.get('tutor_id', '')
                print(f"Processing reply tutor: {tutor_name}")
                try:
                    tutor_data = user_repo.get_user_by_name(tutor_name)
                    tutor_profile_pic = tutor_data.get('profile_picture_url', '') if tutor_data else ''
                    reply['tutor_profile_picture'] = tutor_profile_pic
                    print(f"Reply tutor data for {tutor_name}: {tutor_data}")
                    print(f"Reply tutor profile picture: {tutor_profile_pic}")
                except Exception as e:
                    print(f"Error fetching tutor profile picture for {tutor_name}: {e}")
                    reply['tutor_profile_picture'] = ''
    
    return render_template("index.html", comments=comments) 

@review_bp.route('/send-review/<tutoria_id>', methods=['POST'])
def create_review(tutoria_id):
    firebase_repo = FirebaseTutoringRepository()
    tutoria = firebase_repo.get_tutoria_by_id(tutoria_id)
    return send_review(tutoria)

@review_bp.route("/delete-review/<tutoria_id>/<int:review_id>", methods=["POST"])
def remove_review(tutoria_id, review_id):
    return delete_review(tutoria_id, review_id)

@review_bp.route("/reply-review/<tutoria_id>/<int:review_id>", methods=["POST"])
def reply_review(tutoria_id, review_id):
    return add_reply(tutoria_id, review_id)

@review_bp.route("/edit-review/<tutoria_id>/<int:review_id>", methods=["POST"])
def edit_review_route(tutoria_id, review_id):
    return edit_review(tutoria_id, review_id)

@review_bp.route('/comments/<tutoria_id>')
def comments_by_session(tutoria_id):
    firebase_repo = FirebaseTutoringRepository()
    user_repo = FirebaseUserRepository()
    tutoria = firebase_repo.get_tutoria_by_id(tutoria_id)

    tutor_id = tutoria.tutor
    session_id = tutoria.title
    
    # Get tutor profile picture for header
    tutor_profile_picture = ''
    try:
        tutor_data = user_repo.get_user_by_name(tutor_id)
        tutor_profile_picture = tutor_data.get('profile_picture_url', '') if tutor_data else ''
        print(f"Tutor data for {tutor_id}: {tutor_data}")
        print(f"Tutor profile picture: {tutor_profile_picture}")
    except Exception as e:
        print(f"Error fetching tutor profile picture for {tutor_id}: {e}")
    
    all_reviews = get_all_reviews()
    filtered = [r for r in all_reviews if r['session_id'] == session_id]

    # Enrich comments with user profile pictures
    for comment in filtered:
        # Get student profile picture
        student_name = comment.get('student_id', '')
        print(f"Processing student: {student_name}")
        try:
            student_data = user_repo.get_user_by_name(student_name)
            student_profile_pic = student_data.get('profile_picture_url', '') if student_data else ''
            comment['student_profile_picture'] = student_profile_pic
            print(f"Student data for {student_name}: {student_data}")
            print(f"Student profile picture: {student_profile_pic}")
        except Exception as e:
            print(f"Error fetching student profile picture for {student_name}: {e}")
            comment['student_profile_picture'] = ''
        
        # Get tutor profile picture for replies
        if 'replies' in comment:
            for reply in comment['replies']:
                tutor_name = reply.get('tutor_id', '')
                print(f"Processing reply tutor: {tutor_name}")
                try:
                    reply_tutor_data = user_repo.get_user_by_name(tutor_name)
                    reply_tutor_pic = reply_tutor_data.get('profile_picture_url', '') if reply_tutor_data else ''
                    reply['tutor_profile_picture'] = reply_tutor_pic
                    print(f"Reply tutor data for {tutor_name}: {reply_tutor_data}")
                    print(f"Reply tutor profile picture: {reply_tutor_pic}")
                except Exception as e:
                    print(f"Error fetching tutor profile picture for {tutor_name}: {e}")
                    reply['tutor_profile_picture'] = ''

    # Calculate average and quantity
    average = calculate_average_reviews(filtered)
    quantity = len(filtered)

    if quantity < 10:
        flash("Pocas calificaciones disponibles", "info")

    for c in filtered:
        print("REVIEW:", c)

    return render_template("index.html", 
                         session_id=session_id, 
                         comments=filtered, 
                         tutor_name=tutor_id, 
                         tutoria_id=tutoria_id,
                         tutor_profile_picture=tutor_profile_picture,
                         average=average, 
                         quantity=quantity)

@review_bp.route('/send-review/<tutoria_id>', methods=['POST'])
def create_review_with_session(tutoria_id):
    firebase_repo = FirebaseTutoringRepository()
    tutoria = firebase_repo.get_tutoria_by_id(tutoria_id)
    return send_review(tutoria=tutoria)

@review_bp.route("/edit-reply/<tutoria_id>/<int:review_id>/<int:reply_index>", methods=["POST"])
def edit_reply_route(tutoria_id, review_id, reply_index):
    return edit_reply(tutoria_id, review_id, reply_index)

@review_bp.route("/delete-reply/<tutoria_id>/<int:review_id>/<int:reply_index>", methods=["POST"])
def delete_reply_route(tutoria_id, review_id, reply_index):
    return delete_reply(tutoria_id, review_id, reply_index)
