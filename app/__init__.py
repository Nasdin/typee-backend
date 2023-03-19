from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import auth

from .api import router as api_router

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

# Apply the authentication decorator to all routes in the API router
for route in api_router.routes:
    route.dependencies.append(authenticate_user())

app.include_router(api_router)
