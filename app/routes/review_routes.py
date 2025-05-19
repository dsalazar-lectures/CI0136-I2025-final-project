from flask import Blueprint
from app.controllers.review_controller import send_review, delete_review, add_reply

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/send-review', methods=['POST'])
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
    from app.controllers.review_controller import edit_review
    return edit_review(review_id)
