from flask import Blueprint, render_template

comments_bp = Blueprint(
    'comments', 
    __name__, 
    template_folder='../templates/comments'  
)

@comments_bp.route('/comments')
def index():
    return render_template('index.html', comments=MOCK_COMMENTS) 

MOCK_COMMENTS = [
    {
        'name': 'Ana García',
        'rating': 5,
        'date': '2024-03-20',
        'content': 'Explicaciones muy claras, ¡genial!',
        'reply': {
            'name': 'Tutor Responsable',
            'date': '2024-03-21',
            'content': '¡Gracias Ana! Me alegra que te sirvieran las clases.'
        }
    },
    {
        'name': 'Carlos Méndez',
        'rating': 4,
        'date': '2024-03-19',
        'content': 'Buen tutor pero a veces llega tarde',
        'reply': None
    }
]
