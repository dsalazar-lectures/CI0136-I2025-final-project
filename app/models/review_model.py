import json
import os
from datetime import datetime
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore

# Inicialización de Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Configuración de archivo JSON
JSON_FILE = "reviews_data.json"
JSON_PATH = Path(__file__).parent / "reviews_data.json"

def _load_reviews():
    """Carga las reviews desde el archivo JSON o crea archivo con valores por defecto si no existe"""
    if JSON_PATH.exists():
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)

    default_reviews = [
        {
            'student_id': 'Estudiante Estudiante',
            'rating': 5,
            'date': '05/04/2023',
            'comment': 'Lorem ipsum dolor sit amet...',
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
            'comment': 'Muy buena explicación...',
            'session_id': 'Sesion de Python',
            'review_id': 12345,
            'reply': None
        }
    ]

    save_reviews(default_reviews)
    return default_reviews

def save_review_to_firestore(review):
    """Guarda una review individual en Firestore"""
    try:
        # Convertir nombre de documento (review_id) a int
        review_id_str = str(review['review_id'])
        db.collection('reviews').document(review_id_str).set(review)
    except Exception as e:
        print(f"Error al guardar en Firestore: {e}")

def save_reviews(reviews):
    """Guarda las reviews en el archivo JSON"""
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)

def get_all_reviews():
    return _load_reviews()

def add_review(review):
    reviews = _load_reviews()
    review["date"] = datetime.now().strftime('%d/%m/%Y')
    review["reply"] = None
    reviews.append(review)

    save_reviews(reviews)             # Guarda en archivo local
    save_review_to_firestore(review)  # Guarda en Firebase

def add_reply_to_review(review_id, tutor_id, comment):
    """Añade una respuesta (permite múltiples respuestas)"""
    reviews = _load_reviews()
    for review in reviews:
        if review['review_id'] == review_id:
            # Lista de respuestas
            if 'replies' not in review:
                review['replies'] = []
                
            review['replies'].append({
                'tutor_id': tutor_id,
                'date': datetime.now().strftime('%d/%m/%Y'),
                'comment': comment
            })
            save_reviews(reviews)
            return True
    return False

def get_review_by_id(review_id):
    """Busca una review por ID"""
    reviews = _load_reviews()
    return next((r for r in reviews if r['review_id'] == review_id), None)

def update_review(review_id, new_rating, new_comment):
    reviews = _load_reviews()
    updated = False
    for review in reviews:
        if review['review_id'] == review_id:
            review['rating'] = new_rating
            review['comment'] = new_comment
            review['date'] = datetime.now().strftime('%d/%m/%Y')
            updated = True
            break
    if updated:
        save_reviews(reviews)
    return updated
