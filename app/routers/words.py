from fastapi import APIRouter, Depends, HTTPException
from app.models.word_data import WordData, WordInfo
from app.services.auth import authenticate_user
from app.controllers.safe_word import is_word_safe
from app.controllers.kid_word_encyclopedia import kid_word_encyclopedia

router = APIRouter()


@router.post("/safe", response_model=bool)
async def is_word_safe_route(word_data: WordData, uid: str = Depends(authenticate_user())):
    """
    Check if a given word is safe for children.
    
    Args:
    - word_data (WordData): The input data containing the word to check.
    - uid (str): The unique identifier of the user.
    
    Returns:
    - bool: True if the word is safe, False otherwise.
    
    Raises:
    - HTTPException: If an error occurs during the operation.
    
    Example:
    >>> is_word_safe_route(WordData(word="book"), "user_id")
    True
    """  
    try:
        return await is_word_safe(word_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/encyclopedia", response_model=WordInfo)
async def kid_word_encyclopedia_route(word_data: WordData, uid: str = Depends(authenticate_user())):
    """
    Get detailed information for a given word to help children learn.
    
    Args:
    - word_data (WordData): The input data containing the word to look up.
    - uid (str): The unique identifier of the user.
    
    Returns:
    - WordInfo: The detailed information for the word.
    
    Raises:
    - HTTPException: If an error occurs during the operation.
    
    Example:
    >>> kid_word_encyclopedia_route(WordData(word="book"), "user_id")
    WordInfo(imageUrl='https://example.com/book.jpg', explanation='A book is a collection of written or printed pages that can be read.', story='Once upon a time, there was a girl who loved to read books. She would spend hours lost in different worlds, learning new things, and meeting new characters. Her favorite book was about a little girl who lived in a magical forest.', fact='The first book ever printed was the Gutenberg Bible, printed in 1455.')
    """
    try:
        return await kid_word_encyclopedia(word_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
