from datetime import datetime

reviews = [
    {
        'student_id': 'Estudiante Estudiante',
        'rating': 5,
        'date': '05/04/2023',
        'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, qui iaculis dictum commodo pharetra aliquet a.',
        'session_id': 'Sesion de Python',
        'review_id': 54321,
        'reply': {
            'tutor_id': 'Tutor Tutor',
            'date': '06/04/2023',
            'comment': 'Lorem ipsum dolor sit amet'
        }
    },
    {
        'student_id': 'Estudiante2',
        'rating': 4,
        'date': '10/04/2023',
        'comment': 'Muy buena explicación, pero me hubiera gustado más ejemplos prácticos.',
        'session_id': 'Sesion de Python',
        'review_id': 12345,
        'reply': None
    }
]

def get_all_reviews():
    return reviews

def add_review(review):
    review["date"] = datetime.now().strftime('%d/%m/%Y')
    review["raply"] = None
    reviews.append(review)