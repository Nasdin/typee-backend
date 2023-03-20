from fastapi import APIRouter, Depends, HTTPException
from app.models.word_data import WordData, WordInfo
from app.services.auth import authenticate_user
from app.controllers.safe_word import is_word_safe
from app.controllers.kid_word_encyclopedia import kid_word_encyclopedia

router = APIRouter()


@router.post("/safe", response_model=bool)
async def is_word_safe_route(word_data: WordData, uid: str = Depends(authenticate_user())):
    try:
        return await is_word_safe(word_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/encyclopedia", response_model=WordInfo)
async def kid_word_encyclopedia_route(word_data: WordData, uid: str = Depends(authenticate_user())):
    try:
        return await kid_word_encyclopedia(word_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
