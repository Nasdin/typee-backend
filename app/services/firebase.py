import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firestore
cred = credentials.Certificate("path/to/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_firestore_document(collection: str, document: str):
    doc_ref = db.collection(collection).document(document)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

def set_firestore_document(collection: str, document: str, data: dict):
    doc_ref = db.collection(collection).document(document)
    doc_ref.set(data)