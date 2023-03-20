from typing import List, Dict, Any
from app.services.firebase import (
    get_firestore_collection_by_uid,
    get_firestore_documents_by_uid,
)


async def get_gallery_words(uid: str, limit: int, offset: int) -> List[str]:
    """
    Gets a list of words in the user's gallery.

    Parameters:
    - uid (str): The user's unique identifier.
    - limit (int): The maximum number of words to return.
    - offset (int): The number of words to skip before starting to return results.

    Returns:
    - List[str]: A list of words in the user's gallery.
    """
    # Use the get_firestore_collection_by_uid function
    word_ids = await get_firestore_collection_by_uid("gallery", uid)

    # Apply limit and offset to the list of word_ids
    word_ids = word_ids[offset: offset + limit]

    return word_ids


async def get_gallery_words_detailed(uid: str, limit: int, offset: int) -> List[Dict[str, Any]]:
    """
    Gets detailed information for words in the user's gallery.

    Parameters:
    - uid (str): The user's unique identifier.
    - limit (int): The maximum number of words to return.
    - offset (int): The number of words to skip before starting to return results.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing detailed information for each word in the user's gallery.
    """
    # Use the get_firestore_documents_by_uid function
    word_docs = await get_firestore_documents_by_uid("gallery", uid, limit, offset)

    return word_docs
