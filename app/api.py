# Import the necessary modules, including FastAPI, CORSMiddleware, and the routers.
# Create an instance of the FastAPI app.
# Define a list of allowed origins for CORS.
# Add the CORS middleware to the app, specifying the allowed origins, methods, and headers.
# Initialize Firebase for the application.
# Include the routers for the gallery and word-related routes with their respective prefixes and tags.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin

from app.routers import gallery_router, word_router

app = FastAPI()

# List of allowed origins for CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost",
    "http://localhost:3000",
    # Add any other allowed origins
]

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase
firebase_admin.initialize_app()

# Include the routers for the gallery and word-related routes
app.include_router(gallery_router, prefix="/api/v1/gallery", tags=["gallery"])
app.include_router(word_router, prefix="/api/v1/word", tags=["Words"])