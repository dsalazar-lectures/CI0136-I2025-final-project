import json
import os
from datetime import datetime
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore

class ReviewManager:
    def __init__(self):
        # Inicialización de Firebase
        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase_credentials.json")
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
        self.json_path = Path(__file__).parent / "reviews_data.json"
    
    def _load_reviews(self):
        """Carga las reviews desde el archivo JSON o crea archivo con valores por defecto si no existe"""
        if self.json_path.exists():
            with open(self.json_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        default_reviews = []
        self.save_reviews(default_reviews)
        return default_reviews

    def save_reviews(self, reviews):
        """Guarda las reviews en el archivo JSON"""
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, indent=2, ensure_ascii=False)

    def save_review_to_firestore(self, review):
        """Guarda una review individual en Firestore"""
        try:
            review_id_str = str(review['review_id'])
            self.db.collection('reviews').document(review_id_str).set(review)
        except Exception as e:
            print(f"Error al guardar en Firestore: {e}")

    def get_all_reviews(self):
        """Obtiene todas las reviews desde Firestore"""
        try:
            docs = self.db.collection('reviews').stream()
            reviews = []
            for doc in docs:
                data = doc.to_dict()
                if 'review_id' in data:
                    data['review_id'] = int(data['review_id'])
                reviews.append(data)
            return reviews
        except Exception as e:
            print(f"[ERROR] No se pudieron cargar reviews desde Firestore: {e}")
            return []

    def add_review(self, review):
        reviews = self._load_reviews()
        review["date"] = datetime.now().strftime('%d/%m/%Y')
        reviews.append(review)

        self.save_reviews(reviews)
        self.save_review_to_firestore(review)

    def add_reply_to_review(self, review_id, tutor_id, comment):
        """Añade una respuesta a una review y la sincroniza con Firestore"""
        reviews = self._load_reviews()
        for review in reviews:
            if review['review_id'] == review_id:
                if 'replies' not in review:
                    review['replies'] = []

                new_reply = {
                    'tutor_id': tutor_id,
                    'date': datetime.now().strftime('%d/%m/%Y'),
                    'comment': comment
                }

                review['replies'].append(new_reply)
                self.save_reviews(reviews)

                try:
                    review_id_str = str(review_id)
                    self.db.collection('reviews').document(review_id_str).update({
                        'replies': firestore.ArrayUnion([new_reply])
                    })
                except Exception as e:
                    print(f"Error al actualizar Firestore: {e}")

                return True
        return False

    def get_review_by_id(self, review_id):
        """Obtiene una review individual desde Firestore"""
        try:
            doc_ref = self.db.collection('reviews').document(str(review_id))
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                data['review_id'] = int(data['review_id'])
                return data
            else:
                return None
        except Exception as e:
            print(f"Error al obtener review {review_id} desde Firestore: {e}")
            return None

    def update_review(self, review_id, new_rating, new_comment):
        reviews = self._load_reviews()
        updated = False

        for review in reviews:
            if review['review_id'] == review_id:
                review['rating'] = new_rating
                review['comment'] = new_comment
                review['date'] = datetime.now().strftime('%d/%m/%Y')
                updated = True

                self.save_reviews(reviews)

                try:
                    review_id_str = str(review_id)
                    self.db.collection('reviews').document(review_id_str).update({
                        'rating': new_rating,
                        'comment': new_comment,
                        'date': review['date']
                    })
                except Exception as e:
                    print(f"Error al actualizar review en Firestore: {e}")
                break

        return updated

    def delete_review(self, review_id):
        reviews = self._load_reviews()
        new_reviews = [r for r in reviews if r['review_id'] != review_id]

        if len(new_reviews) == len(reviews):
            print(f"[WARN] Review con ID {review_id} no encontrada en JSON")
            return False

        self.save_reviews(new_reviews)

        try:
            review_id_str = str(review_id)
            doc_ref = self.db.collection('reviews').document(review_id_str)
            if doc_ref.get().exists:
                doc_ref.delete()
                print(f"[OK] Review {review_id} eliminada de Firestore")
            else:
                print(f"[WARN] Review con ID {review_id} no existe en Firestore")
        except Exception as e:
            print(f"[ERROR] Error al eliminar review en Firestore: {e}")

        return True

# Create a singleton instance
review_manager = ReviewManager()

# Facade functions that delegate to the ReviewManager
def get_all_reviews():
    return review_manager.get_all_reviews()

def add_review(review):
    return review_manager.add_review(review)

def add_reply_to_review(review_id, tutor_id, comment):
    return review_manager.add_reply_to_review(review_id, tutor_id, comment)

def get_review_by_id(review_id):
    return review_manager.get_review_by_id(review_id)

def update_review(review_id, new_rating, new_comment):
    return review_manager.update_review(review_id, new_rating, new_comment)

def delete_review(review_id):
    return review_manager.delete_review(review_id)

def save_reviews(reviews):
    return review_manager.save_reviews(reviews)

def save_review_to_firestore(review):
    return review_manager.save_review_to_firestore(review)