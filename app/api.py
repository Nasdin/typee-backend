from typing import Optional

import firebase_admin
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import auth

from .api.kid_word_encyclopedia import kid_word_encyclopedia
from .api.safe_word import is_word_safe
from .models.word_data import WordData, WordInfo

router = APIRouter()


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
            authorization_header = kwargs.get("request").headers.get("Authorization")
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


@router.post("/is-word-safe", response_model=bool)
async def is_word_safe_route(word_data: WordData, request: Request, uid: Optional[str] = Depends(authenticate_user())):
    """
    API endpoint to check if a word is safe for children.

    Args:
        word_data (WordData): A Pydantic model containing the word to be checked.
        request (Request): The request object.
        uid (Optional[str], optional): User ID of the authenticated user. Defaults to None.

    Returns:
        A boolean value indicating whether the word is safe or not.

    Example:
        >>> word_data = WordData(word="apple")
        >>> response = await is_word_safe_route(word_data, Request)
        >>> assert response == True
    """
    return await is_word_safe(word_data)


@router.post("/kid-word-encyclopedia", response_model=WordInfo)
async def kid_word_encyclopedia_route(word_data: WordData, request: Request,
                                      uid: Optional[str] = Depends(authenticate_user())):
    """
    API endpoint to generate information about a word suitable for children.

    Args:
        word_data (WordData): A Pydantic model containing the word to generate information for.
        request (Request): The request object.
        uid (Optional[str], optional): User ID of the authenticated user. Defaults to None.

    Returns:
        A Pydantic model containing information about the word suitable for children.

    Example:
        >>> word_data = WordData(word="apple")
        >>> response = await kid_word_encyclopedia_route(word_data, Request)
        >>> assert response.imageUrl is not None
        >>> assert response.explanation is not None
        >>> assert response.story is not None
        >>> assert response.fact is not None
    """
    return await kid_word_encyclopedia(word_data)


# Apply the authentication decorator to all routes in the API router
for route in router.routes:
    route.dependencies.append(authenticate_user())

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    # Add any other allowed origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase
firebase_admin.initialize_app()

app.include_router(router)
