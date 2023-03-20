from app.services.firebase import (
    get_firestore_collection_by_uid,
    get_firestore_documents_by_uid,
)
from app.models.word_data import WordDetailsListResponse, WordListResponse, WordInfo, GalleryWordsQueryParams


async def get_gallery_words(uid: str, params: GalleryWordsQueryParams) -> WordListResponse:
    """
    Gets a list of words in the user's gallery.

    Parameters:
    - uid (str): The user's unique identifier.
    - limit (int): The maximum number of words to return.
    - offset (int): The number of words to skip before starting to return results.

    Returns:
    - WordListResponse: A response containing a list of words in the user's gallery.
    """
    # Use the get_firestore_collection_by_uid function
    words = await get_firestore_collection_by_uid("gallery", uid, "word")

    # Apply limit and offset to the list of word_ids
    words = words[params.offset: params.offset + params.limit]

    return WordListResponse(words=words)


async def get_gallery_words_detailed(uid: str, params: GalleryWordsQueryParams) -> WordDetailsListResponse:
    """
    Gets detailed information for words in the user's gallery.

    Parameters:
    - uid (str): The user's unique identifier.
    - limit (int): The maximum number of words to return.
    - offset (int): The number of words to skip before starting to return results.

    Returns:
    - WordDetailsListResponse: A response containing a list of dictionaries containing detailed information for each word in the user's gallery.
    """
    # Use the get_firestore_documents_by_uid function
    word_docs = await get_firestore_documents_by_uid("gallery", uid, params.limit, params.offset)

    # Convert the list of dictionaries to a list of WordInfo objects
    words_info = [WordInfo(**word_doc) for word_doc in word_docs]

    return WordDetailsListResponse(words=words_info)
