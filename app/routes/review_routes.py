from flask import Blueprint, render_template
from app.models.review_model import get_all_reviews
from app.controllers.review_controller import send_review, delete_review, add_reply, edit_review

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/comments/')
def home():
    comments = get_all_reviews()
    return render_template("index.html", comments=comments) 

@review_bp.route('/send-review/', methods=['POST'])
def create_review():
     return send_review()

@review_bp.route("/delete-review/<int:review_id>", methods=["POST"])
def remove_review(review_id):
    return delete_review(review_id)

@review_bp.route("/reply-review/<int:review_id>", methods=["POST"])
def reply_review(review_id):
    return add_reply(review_id)

@review_bp.route("/edit-review/<int:review_id>", methods=["POST"])
def edit_review_route(review_id):
    return edit_review(review_id)

@review_bp.route('/comments/<session_id>')
def comments_by_session(session_id):
    all_reviews = get_all_reviews()
    filtered = [r for r in all_reviews if r['session_id'] == session_id]
    return render_template("index.html", comments=filtered, session_id=session_id)

@review_bp.route('/send-review/<session_id>', methods=['POST'])
def create_review_with_session(session_id):
    return send_review(session_id=session_id)
