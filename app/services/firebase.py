import asyncio
import os

import firebase_admin
from firebase_admin import credentials, firestore, auth
from typing import List, Dict, Any

# Get the path to the Firebase credentials file from the environment variable
cred_path = os.environ.get("FIREBASE_ADMINSDK_JSON_FILE")

# Initialize Firestore with the credentials
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()


async def get_firestore_document(collection: str, document: str):
    """
    Gets a document from a specified Firestore collection.

    Args:
        collection (str): The name of the Firestore collection to retrieve the document from.
        document (str): The name of the document to retrieve.

    Returns:
        A dictionary containing the document data, or None if the document does not exist.
    """
    doc_ref = db.collection(collection).document(document)

    # Use a thread to run synchronous code
    loop = asyncio.get_event_loop()
    doc = await loop.run_in_executor(None, lambda: doc_ref.get())

    if doc.exists:
        return doc.to_dict()
    else:
        return None


async def set_firestore_document(collection: str, document: str, data: dict):
    """
        Sets a document in a specified Firestore collection.

        Args:
            collection (str): The name of the Firestore collection to set the document in.
            document (str): The name of the document to set.
            data (dict): A dictionary containing the data to set in the document.

        Returns:
            None
        """
    doc_ref = db.collection(collection).document(document)

    # Use a thread to run synchronous code
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: doc_ref.set(data))


async def get_firestore_collection_by_uid(collection: str, uid: str, attribute: str) -> List[str]:
    query = db.collection(collection).where("uid", "==", uid)

    # Use a thread to run synchronous code
    loop = asyncio.get_event_loop()
    docs = await loop.run_in_executor(None, lambda: query.stream())

    return [doc.get(attribute) for doc in docs]


async def get_firestore_documents_by_uid(collection: str, uid: str, limit: int, offset: int) -> List[Dict[str, Any]]:
    query = db.collection(collection).where(
        "uid", "==", uid).offset(offset).limit(limit)

    # Use a thread to run synchronous code
    loop = asyncio.get_event_loop()
    docs = await loop.run_in_executor(None, lambda: query.stream())

    return [doc.to_dict() for doc in docs]


def authenticate_user():
    """
    A decorator function to check for authenticated users.

    Returns:
        Wrapped function.

    Example:
        >>> @authenticate_user()
        ... async def wrapped(*args, **kwargs):
        ...     # do something
        ...     pass
    """

    def wrapper(func):
        async def wrapped(*args, **kwargs):
            authorization_header = kwargs.get(
                "request").headers.get("Authorization")
            if authorization_header is None:
                return {"error": "Unauthorized"}, 401

            try:
                token = authorization_header.split(" ")[1]
                decoded_token = auth.verify_id_token(token)
                kwargs["uid"] = decoded_token.get("uid")
            except:
                return {"error": "Unauthorized"}, 401

            return await func(*args, **kwargs)

        return wrapped

    return wrapper
