from fastapi import APIRouter, Depends
from app.models.word_data import WordListResponse, WordDetailsListResponse, GalleryWordsQueryParams
from app.services.firebase import authenticate_user
from app.controllers import get_gallery_words, get_gallery_words_detailed


router = APIRouter()


@router.get("/words", response_model=WordListResponse)
async def get_words(
    query_params: GalleryWordsQueryParams = Depends(),
    uid: str = Depends(authenticate_user())
) -> WordListResponse:
    """
    Gets a list of words in the user's gallery.

    Parameters:
    - query_params (GalleryWordsQueryParams): A Pydantic model for query parameters including limit and offset.
    - uid (str): The user's unique identifier.

    Returns:
    - WordListResponse: A response containing a list of words in the user's gallery.
    """
    words = await get_gallery_words(uid, query_params)
    return words


@router.get("/words_detailed", response_model=WordDetailsListResponse)
async def get_words_detailed(
    query_params: GalleryWordsQueryParams = Depends(),
    uid: str = Depends(authenticate_user())
) -> WordDetailsListResponse:
    """
    Gets detailed information for words in the user's gallery.

    Parameters:
    - query_params (GalleryWordsQueryParams): A Pydantic model for query parameters including limit and offset.
    - uid (str): The user's unique identifier.

    Returns:
    - WordDetailsListResponse: A response containing a list of dictionaries containing detailed information for each word in the user's gallery.
    """
    word_docs = await get_gallery_words_detailed(uid, query_params)
    return word_docs
