from flask import Blueprint, render_template
from app.models.review_model import get_all_reviews
from app.controllers.review_controller import send_review, delete_review, add_reply, edit_review
from app.models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/comments/')
def home():
    comments = get_all_reviews()
    return render_template("index.html", comments=comments) 

@review_bp.route('/send-review/', methods=['POST'])
def create_review():
     return send_review()

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
    tutoria = firebase_repo.get_tutoria_by_id(tutoria_id)

    tutor_id = tutoria.tutor
    session_id = tutoria.title
    
    all_reviews = get_all_reviews()
    filtered = [r for r in all_reviews if r['session_id'] == session_id]

    return render_template("index.html", session_id=session_id, comments=filtered, tutor_name=tutor_id, tutoria_id=tutoria_id)

@review_bp.route('/send-review/<tutoria_id>', methods=['POST'])
def create_review_with_session(tutoria_id):
    firebase_repo = FirebaseTutoringRepository()
    tutoria = firebase_repo.get_tutoria_by_id(tutoria_id)

    #tutor_id = tutoria.tutor
    #session_id = tutoria.title
    return send_review(tutoria=tutoria)
