from typing import Optional

import firebase_admin
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.gallery_words import router as gallery_router
from .routers.words import router as word_router


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


app.include_router(gallery_router, prefix="/api/v1/gallery",
                   tags=["gallery"])
app.include_router(word_router, prefix="/api/v1/word", tags=["Words"])
