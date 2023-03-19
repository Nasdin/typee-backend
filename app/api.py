from fastapi import APIRouter, Depends, Request
from typing import Optional

from .api.safe_word import is_word_safe
from .api.kid_word_encyclopedia import kid_word_encyclopedia
from .models.word_data import WordData, WordInfo
from . import authenticate_user

router = APIRouter()

@router.post("/is-word-safe", response_model=bool)
async def is_word_safe_route(word_data: WordData, request: Request, uid: Optional[str] = Depends(authenticate_user())):
    return await is_word_safe(word_data)

@router.post("/kid-word-encyclopedia", response_model=WordInfo)
async def kid_word_encyclopedia_route(word_data: WordData, request: Request, uid: Optional[str] = Depends(authenticate_user())):
    return await kid_word_encyclopedia(word_data)
