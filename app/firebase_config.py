import firebase_admin
from firebase_admin import credentials, firestore, auth
db = None

def initialize_firebase():
    global db
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebaseAccountKey.json")  # 🔒 archivo correcto
        firebase_admin.initialize_app(cred)
    db = firestore.client()

def get_db():
    return db