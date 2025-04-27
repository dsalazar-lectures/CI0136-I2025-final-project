from flask import Blueprint, render_template, request, redirect, url_for, flash

home = Blueprint('home', __name__)

@home.route("/")
@home.route('/<name>')
def greeting(name=None):
    return render_template('home.html', person=name)

@home.route("/")
def index():
    return redirect(url_for('home.comments'))  # Redirige a comentarios

# New comments route
@home.route('/comments')
def comments():
    # Mock Data 
    comments = [
        {
            'name': 'Juan Pérez',
            'rating': 5,
            'date': '2024-03-15',
            'content': 'Excelente tutor, muy paciente.',
            'reply': {
                'name': 'Tutor Tutor',
                'date': '2024-03-16',
                'content': '¡Gracias por tus palabras!'
            }
        }
    ]
    return render_template('index.html', comments=comments)

# Review route
@home.route('/comments/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment', '').strip()
        
        if not rating:
            flash('Debes seleccionar una calificación', 'danger')
            return redirect(url_for('home.review'))
        
        # TODO: Data Base implementation
        flash('Reseña enviada exitosamente', 'success')
        return redirect(url_for('home.comments'))
    
    return render_template('review.html')