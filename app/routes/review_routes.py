from flask import Blueprint
from controllers.review_controller import send_review, delete_review

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/send-review', methods=['POST'])
def create_review():
    return send_review()

@review_bp.route("/delete-review/<int:review_id>", methods=["POST"])
def remove_review(review_id):
    return delete_review(review_id)