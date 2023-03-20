from fastapi import APIRouter, Depends, Query, Request
from app.services.firebase import authenticate_user
from app.controllers import get_gallery_words, get_gallery_words_detailed


router = APIRouter()


@router.get("/words")
async def get_words(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    request: Request = Depends(),
    uid: str = Depends(authenticate_user())
):
    words = await get_gallery_words(uid, limit, offset)
    return {"words": words}


@router.get("/words_detailed")
async def get_words_detailed(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    request: Request = Depends(),
    uid: str = Depends(authenticate_user())
):
    word_details = await get_gallery_words_detailed(uid, limit, offset)
    return {"words": word_details}
