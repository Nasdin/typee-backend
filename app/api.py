from typing import Optional

import firebase_admin
from fastapi import APIRouter, Depends, Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import auth

from .api.kid_word_encyclopedia import kid_word_encyclopedia
from .api.safe_word import is_word_safe
from .models.word_data import WordData, WordInfo

router = APIRouter()


# Define a decorator function to check for authenticated users
def authenticate_user():
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
    return await is_word_safe(word_data)


@router.post("/kid-word-encyclopedia", response_model=WordInfo)
async def kid_word_encyclopedia_route(word_data: WordData, request: Request,
                                      uid: Optional[str] = Depends(authenticate_user())):
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
