from flask import Blueprint, render_template

comments_bp = Blueprint(
    'comments', 
    __name__, 
    template_folder='../templates/comments'  
)

@comments_bp.route('/comments')
def index():
    return render_template('index.html')  