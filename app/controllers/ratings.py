from flask import Blueprint, render_template, request, redirect, url_for, flash

ratings_bp = Blueprint(
    'ratings', 
    __name__, 
    template_folder='../templates/ratings/' 
)

@ratings_bp.route('/review')
def review():
    return render_template('review.html')  