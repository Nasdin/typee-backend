import os
import asyncio

import firebase_admin
from firebase_admin import credentials, firestore

# Get the path to the Firebase credentials file from the environment variable
cred_path = os.environ.get("FIREBASE_ADMINSDK_JSON_FILE")

# Initialize Firestore with the credentials
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()


async def get_firestore_document(collection: str, document: str):
    doc_ref = db.collection(collection).document(document)

    # Use a thread to run synchronous code
    loop = asyncio.get_event_loop()
    doc = await loop.run_in_executor(None, lambda: doc_ref.get())

    if doc.exists:
        return doc.to_dict()
    else:
        return None


async def set_firestore_document(collection: str, document: str, data: dict):
    doc_ref = db.collection(collection).document(document)

    # Use a thread to run synchronous code
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: doc_ref.set(data))
