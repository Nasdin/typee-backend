import firebase_admin
from firebase_admin import credentials, firestore
import os

# Get the path to the Firebase credentials file from the environment variable
cred_path = os.environ.get("FIREBASE_ADMINSDK_JSON_FILE")

# Initialize Firestore with the credentials
cred = credentials.Certificate(cred_path)
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
